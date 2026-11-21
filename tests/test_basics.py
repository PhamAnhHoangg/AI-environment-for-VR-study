"""Light tests that run without the heavy packages (torch, whisper, gradio) and without Unity or a headset."""
import importlib, json, os, re, sys, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")


class RoomConfigTest(unittest.TestCase):
    def setUp(self):
        self.cfg = json.loads((ROOT / "room_config.json").read_text(encoding="utf-8"))

    def test_palette_colors(self):
        for key in ("wall", "ceiling", "floor"):
            self.assertRegex(self.cfg["palette"][key], HEX, key)

    def test_objects_have_german_and_english(self):
        for slot, obj in self.cfg["objects"].items():
            # corner slots choose an object type; table, chairs and door are fixed and have none
            fields = ("type", "german", "english") if slot.startswith("corner") else ("german", "english")
            for field in fields:
                self.assertTrue(str(obj.get(field, "")).strip(), f"{slot} is missing {field}")

    def test_german_nouns_have_an_article(self):
        # the quiz teaches the article together with the noun
        for slot, obj in self.cfg["objects"].items():
            self.assertRegex(obj["german"], r"^(der|die|das) ", f"{slot}: {obj['german']}")


class ColorFetcherTest(unittest.TestCase):
    def setUp(self):
        import color_fetcher
        self.cf = color_fetcher

    def test_brightness(self):
        self.assertTrue(self.cf._is_bright("#FFFFFF"))
        self.assertFalse(self.cf._is_bright("#202020"))
        self.assertFalse(self.cf._is_bright("not a colour"))

    def test_hex_in_css(self):
        self.assertEqual(self.cf._parse_hex_from_style("background: #A1B2C3; color:#ffffff"), ["A1B2C3", "ffffff"])

    def test_offline_pool_is_bright(self):
        pool = self.cf.fetch_bright_colors(try_live=False)
        self.assertTrue(pool)
        self.assertTrue(all(self.cf._is_bright(c) for c in pool))

    def test_room_rule_walls_equal_ceiling(self):
        p = self.cf.randomize_room_colors(try_live=False)
        self.assertEqual(p["wall"], p["ceiling"])
        self.assertTrue(self.cf._is_bright(p["wall"]))

    def test_apply_keeps_other_fields(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "room_config.json")
            Path(path).write_text(json.dumps({"room_type": "X", "objects": {"a": 1}}), encoding="utf-8")
            out = self.cf.apply_colors_to_config(path, {"wall": "#EEEEEE", "floor": "#8B4550", "ceiling": "#EEEEEE"})
            saved = json.loads(Path(path).read_text(encoding="utf-8"))
            self.assertEqual(saved["objects"], {"a": 1})
            self.assertEqual(saved["palette"]["wall"], "#EEEEEE")
            self.assertEqual(out["palette"], saved["palette"])


class VrConfigTest(unittest.TestCase):
    def test_env_overrides(self):
        os.environ["OLLAMA_MODEL"] = "test-model"; os.environ["VR_BIND_HOST"] = "0.0.0.0"
        import vr_config
        importlib.reload(vr_config)
        self.assertEqual(vr_config.OLLAMA_MODEL, "test-model")
        self.assertEqual(vr_config.BIND_HOST, "0.0.0.0")
        del os.environ["OLLAMA_MODEL"]; del os.environ["VR_BIND_HOST"]
        importlib.reload(vr_config)
        self.assertEqual(vr_config.BIND_HOST, "127.0.0.1")   # safe default: this computer only


if __name__ == "__main__":
    unittest.main()
