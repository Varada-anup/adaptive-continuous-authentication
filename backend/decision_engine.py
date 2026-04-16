import numpy as np
import json
import os

PROFILE_PATH = "profiles.json"

class DecisionEngine:
    def __init__(self):
        self.user_profiles = self.load_profiles()
        self.strikes = {}

    def load_profiles(self):
        if os.path.exists(PROFILE_PATH):
            with open(PROFILE_PATH, "r") as f:
                return json.load(f)
        return {}

    def save_profiles(self):
        with open(PROFILE_PATH, "w") as f:
            json.dump(self.user_profiles, f, indent=4)

    def reset_user(self, username):
        self.strikes[username] = 0

    # ---------------- CALIBRATION ----------------

    def start_calibration(self, username):
        self.user_profiles[username] = {
            "samples": [],
            "mean": None,
            "std": None,
            "threshold": None
        }

    def add_calibration_sample(self, username, feature_vector):
        self.user_profiles[username]["samples"].append(feature_vector)

    def finalize_calibration(self, username):
        samples = np.array(self.user_profiles[username]["samples"])

        mean = np.mean(samples, axis=0)
        std = np.std(samples, axis=0) + 1e-6

        normalized = (samples - mean) / std

        scores = []
        for vec in normalized:
            dist = np.linalg.norm(vec)
            score = 1 / (1 + dist)
            scores.append(score)

        threshold = np.percentile(scores, 10)

        self.user_profiles[username].update({
            "mean": mean.tolist(),
            "std": std.tolist(),
            "threshold": float(threshold)
        })

        del self.user_profiles[username]["samples"]
        self.save_profiles()

    # ---------------- AUTH ----------------

    def authenticate(self, username, feature_vector):
        profile = self.user_profiles[username]

        mean = np.array(profile["mean"])
        std = np.array(profile["std"])
        threshold = profile["threshold"]

        norm_vec = (np.array(feature_vector) - mean) / std

        dist = np.linalg.norm(norm_vec)
        score = 1 / (1 + dist)

        if username not in self.strikes:
            self.strikes[username] = 0

        # ---------------- STRIKE LOGIC ----------------

        if score < threshold:
            self.strikes[username] += 1
        else:
            self.strikes[username] = max(0, self.strikes[username] - 2)

        # ---------------- DECISION STATES ----------------

        if self.strikes[username] >= 5:
            decision = "intruder"
        elif score < threshold:
            decision = "suspicious"
        else:
            decision = "genuine"

        # ---------------- ADAPTIVE LEARNING ----------------

        if decision == "genuine" and score > threshold + 0.05:
            self.update_profile(username, feature_vector)

        print(f"[AUTH] {username} | score={score:.3f} | threshold={threshold:.3f} | strikes={self.strikes[username]} | decision={decision}")

        return decision, score

    def update_profile(self, username, feature_vector):
        profile = self.user_profiles[username]

        mean = np.array(profile["mean"])
        new_vec = np.array(feature_vector)

        updated_mean = 0.95 * mean + 0.05 * new_vec

        profile["mean"] = updated_mean.tolist()
        self.save_profiles()