import json
import os

SCORES_FILE = "scores.json"


class ScoreManager:
    def __init__(self, filename=SCORES_FILE):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump([], f)

    def read_scores(self):
        """Read all scores from JSON file"""
        with open(self.filename, "r") as f:
            return json.load(f)

    def create_score(self, name, score):
        """Add a new score"""
        scores = self.read_scores()
        scores.append({"name": name, "score": score})
        self._save(scores)

    def update_score(self, name, new_score):
        """Update score if higher"""
        scores = self.read_scores()
        for s in scores:
            if s["name"] == name:
                if new_score > s["score"]:
                    s["score"] = new_score
                break
        else:
            # if name not found, create new
            scores.append({"name": name, "score": new_score})
        self._save(scores)

    def delete_score(self, name):
        """Delete a score by name"""
        scores = self.read_scores()
        scores = [s for s in scores if s["name"] != name]
        self._save(scores)

    def _save(self, scores):
        with open(self.filename, "w") as f:
            json.dump(scores, f, indent=4)

    def top_scores(self, n=5):
        """Get top n scores"""
        scores = self.read_scores()
        return sorted(scores, key=lambda x: x["score"], reverse=True)[:n]
