#!/usr/bin/env python3
"""Experiment 3: VLM Zero-Shot Energy Infrastructure Inspection with CLIP.

Uses the ELPV (Electroluminescence Photovoltaic) dataset of solar cell images.
Tests zero-shot CLIP classification vs simple supervised baseline.
"""
import os, sys, time, json
import numpy as np
import warnings
warnings.filterwarnings("ignore")

np.random.seed(42)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "codes", "results")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

# ELPV dataset from cloned repo
ELPV_DIR = os.path.join(DATA_DIR, "elpv_repo", "src", "elpv_dataset", "data")


def load_elpv_data(max_per_class=150):
    """Load ELPV images and labels from cloned repo."""
    from PIL import Image
    from collections import Counter

    labels_file = os.path.join(ELPV_DIR, "labels.csv")
    img_dir = ELPV_DIR

    if not os.path.exists(labels_file):
        print(f"ERROR: Labels file not found at {labels_file}")
        print("Please clone the ELPV dataset first:")
        print("  cd data && git clone --depth 1 https://github.com/zae-bayern/elpv-dataset.git elpv_repo")
        return [], []

    # Parse labels file (format: "images/cellNNNN.png  LABEL  TYPE")
    entries = []
    with open(labels_file) as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                img_name = parts[0]
                label = float(parts[1])
                entries.append((img_name, label))

    # Sample balanced subset: binary classification (0 = functional, >0 = defective)
    functional = [(n, l) for n, l in entries if l == 0]
    defective = [(n, l) for n, l in entries if l > 0]

    np.random.shuffle(functional)
    np.random.shuffle(defective)
    functional = functional[:max_per_class]
    defective = defective[:max_per_class]

    selected = functional + defective
    np.random.shuffle(selected)

    images = []
    labels = []
    for img_name, label in selected:
        img_path = os.path.join(img_dir, img_name)
        if os.path.exists(img_path):
            try:
                img = Image.open(img_path).convert("RGB")
                images.append(img)
                labels.append(1 if label > 0 else 0)
            except Exception:
                pass

    n_func = sum(1 for l in labels if l == 0)
    n_def = sum(1 for l in labels if l == 1)
    print(f"Loaded {len(images)} images: {n_func} functional, {n_def} defective")
    return images, labels


def run_clip_zeroshot(images, labels, prompt_set="generic"):
    """Run zero-shot CLIP classification."""
    import torch
    import open_clip
    print(f"\nRunning CLIP zero-shot ({prompt_set} prompts)...")
    t0 = time.time()

    model, _, preprocess = open_clip.create_model_and_transforms(
        "ViT-B-32", pretrained="laion2b_s34b_b79k")
    tokenizer = open_clip.get_tokenizer("ViT-B-32")

    # Define text prompts
    if prompt_set == "generic":
        prompts = {
            0: [
                "a photo of a functional solar cell",
                "a photo of a healthy photovoltaic cell with no defects",
                "an electroluminescence image of a working solar cell",
            ],
            1: [
                "a photo of a defective solar cell",
                "a photo of a damaged photovoltaic cell with cracks",
                "an electroluminescence image of a broken solar cell",
            ],
        }
    elif prompt_set == "domain":
        prompts = {
            0: [
                "electroluminescence image showing uniform brightness in a solar cell",
                "a photovoltaic cell with even light emission indicating good health",
                "a solar cell with no dark areas or cracks in EL imaging",
            ],
            1: [
                "electroluminescence image showing dark areas or cracks in a solar cell",
                "a photovoltaic cell with uneven brightness indicating defects",
                "a solar cell with visible fractures or inactive regions in EL imaging",
            ],
        }
    elif prompt_set == "ensemble":
        prompts = {
            0: [
                "a photo of a functional solar cell",
                "a healthy photovoltaic cell with no defects",
                "electroluminescence image showing uniform brightness",
                "a solar cell with even light emission",
                "a working solar panel cell",
            ],
            1: [
                "a photo of a defective solar cell",
                "a damaged photovoltaic cell with cracks",
                "electroluminescence image showing dark areas or cracks",
                "a solar cell with uneven brightness indicating defects",
                "a broken solar panel cell with fractures",
            ],
        }

    # Encode text prompts
    text_features = {}
    for cls, texts in prompts.items():
        tokens = tokenizer(texts)
        with torch.no_grad():
            feats = model.encode_text(tokens)
            feats /= feats.norm(dim=-1, keepdim=True)
            text_features[cls] = feats.mean(dim=0)
            text_features[cls] /= text_features[cls].norm()

    # Classify each image
    predictions = []
    confidences = []
    all_sims = []
    for img in images:
        img_tensor = preprocess(img).unsqueeze(0)
        with torch.no_grad():
            img_feat = model.encode_image(img_tensor)
            img_feat /= img_feat.norm(dim=-1, keepdim=True)

        sims = {}
        for cls, text_feat in text_features.items():
            sim = (img_feat @ text_feat.unsqueeze(-1)).squeeze().item()
            sims[cls] = sim

        pred = max(sims, key=sims.get)
        predictions.append(pred)
        all_sims.append(sims)

        # Confidence via softmax of similarities (temperature=100)
        exp_sims = {k: np.exp(v * 100) for k, v in sims.items()}
        total = sum(exp_sims.values())
        confidences.append(exp_sims[pred] / total)

    elapsed = time.time() - t0
    return predictions, confidences, all_sims, elapsed


def run_supervised_baseline(images, labels):
    """Supervised baseline: CLIP features + logistic regression."""
    import torch
    import open_clip
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import StratifiedKFold, cross_val_predict
    print("\nRunning supervised baseline (CLIP features + LogReg, 5-fold CV)...")
    t0 = time.time()

    model, _, preprocess = open_clip.create_model_and_transforms(
        "ViT-B-32", pretrained="laion2b_s34b_b79k")

    # Extract features
    features = []
    for img in images:
        img_tensor = preprocess(img).unsqueeze(0)
        with torch.no_grad():
            feat = model.encode_image(img_tensor).squeeze().numpy()
        features.append(feat)
    features = np.array(features)
    labels_arr = np.array(labels)

    # 5-fold stratified cross-validation
    clf = LogisticRegression(max_iter=1000, random_state=42, C=1.0)
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    preds = cross_val_predict(clf, features, labels_arr, cv=cv)

    elapsed = time.time() - t0
    return preds, elapsed


def run_random_baseline(labels):
    """Random baseline for reference."""
    preds = np.random.randint(0, 2, size=len(labels))
    return preds


def compute_classification_metrics(labels, predictions):
    """Compute accuracy, precision, recall, F1."""
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

    labels = np.array(labels)
    predictions = np.array(predictions)
    min_len = min(len(labels), len(predictions))
    labels = labels[:min_len]
    predictions = predictions[:min_len]

    return {
        "accuracy": round(accuracy_score(labels, predictions), 4),
        "precision": round(precision_score(labels, predictions, zero_division=0), 4),
        "recall": round(recall_score(labels, predictions, zero_division=0), 4),
        "f1": round(f1_score(labels, predictions, zero_division=0), 4),
        "n_samples": int(min_len),
    }


def main():
    print("=" * 60)
    print("EXPERIMENT 3: VLM Zero-Shot Solar Panel Inspection")
    print("=" * 60)

    images, labels = load_elpv_data(max_per_class=150)

    if not images:
        print("ERROR: No images loaded. Exiting.")
        return

    results = {}

    # 0. Random baseline
    preds_random = run_random_baseline(labels)
    results["Random baseline"] = compute_classification_metrics(labels, preds_random)
    print(f"\nRandom baseline: {results['Random baseline']}")

    # 1. CLIP zero-shot (generic prompts)
    preds_generic, confs_generic, sims_generic, t1 = run_clip_zeroshot(
        images, labels, "generic")
    results["CLIP zero-shot (generic)"] = {
        **compute_classification_metrics(labels, preds_generic),
        "time_sec": round(t1, 1),
        "avg_confidence": round(float(np.mean(confs_generic)), 4),
    }
    print(f"CLIP generic: {results['CLIP zero-shot (generic)']}")

    # 2. CLIP zero-shot (domain-specific prompts)
    preds_domain, confs_domain, sims_domain, t2 = run_clip_zeroshot(
        images, labels, "domain")
    results["CLIP zero-shot (domain)"] = {
        **compute_classification_metrics(labels, preds_domain),
        "time_sec": round(t2, 1),
        "avg_confidence": round(float(np.mean(confs_domain)), 4),
    }
    print(f"CLIP domain: {results['CLIP zero-shot (domain)']}")

    # 3. CLIP zero-shot (ensemble prompts)
    preds_ensemble, confs_ensemble, sims_ensemble, t3 = run_clip_zeroshot(
        images, labels, "ensemble")
    results["CLIP zero-shot (ensemble)"] = {
        **compute_classification_metrics(labels, preds_ensemble),
        "time_sec": round(t3, 1),
        "avg_confidence": round(float(np.mean(confs_ensemble)), 4),
    }
    print(f"CLIP ensemble: {results['CLIP zero-shot (ensemble)']}")

    # 4. Supervised baseline (CLIP features + LogReg, 5-fold CV)
    preds_sup, t4 = run_supervised_baseline(images, labels)
    results["Supervised (CLIP+LogReg)"] = {
        **compute_classification_metrics(labels, preds_sup),
        "time_sec": round(t4, 1),
        "note": "5-fold stratified cross-validation",
    }
    print(f"Supervised: {results['Supervised (CLIP+LogReg)']}")

    # Print comparison table
    print(f"\n{'=' * 60}")
    print("RESULTS COMPARISON")
    print(f"{'=' * 60}")
    print(f"{'Model':32s} {'Acc':>7s} {'Prec':>7s} {'Recall':>7s} {'F1':>7s}")
    print("-" * 65)
    for model, metrics in results.items():
        print(f"{model:32s} {metrics['accuracy']:7.4f} "
              f"{metrics['precision']:7.4f} {metrics['recall']:7.4f} "
              f"{metrics['f1']:7.4f}")

    # Compute confusion matrices for the best zero-shot model
    from sklearn.metrics import confusion_matrix
    best_zs = "CLIP zero-shot (ensemble)"
    cm = confusion_matrix(labels, preds_ensemble).tolist()
    results["confusion_matrix_ensemble"] = cm

    # Dataset stats
    results["dataset"] = {
        "name": "ELPV (Electroluminescence Photovoltaic)",
        "total_images": len(images),
        "functional": sum(1 for l in labels if l == 0),
        "defective": sum(1 for l in labels if l == 1),
        "source": "https://github.com/zae-bayern/elpv-dataset",
    }

    # Save results
    output = os.path.join(RESULTS_DIR, "vlm_inspection.json")
    with open(output, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {output}")

    return results


if __name__ == "__main__":
    main()
