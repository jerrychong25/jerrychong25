from pathlib import Path
import re
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
README_PATH = REPO_ROOT / "README.md"
SVG_PATH = REPO_ROOT / "github-metrics.svg"
WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "main.yml"


class TestSEOStandards(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.readme = README_PATH.read_text(encoding="utf-8")
        cls.svg = SVG_PATH.read_text(encoding="utf-8")
        cls.workflow = WORKFLOW_PATH.read_text(encoding="utf-8")
        cls.readme_lower = cls.readme.lower()

    def test_readme_has_single_primary_heading(self):
        html_h1_matches = re.findall(r"<h1\b[^>]*>.*?</h1>", self.readme, flags=re.IGNORECASE | re.DOTALL)
        markdown_h1_matches = re.findall(r"^#\s+.+$", self.readme, flags=re.MULTILINE)
        total_h1 = len(html_h1_matches) + len(markdown_h1_matches)
        self.assertEqual(total_h1, 1, "README should expose exactly one primary H1 heading.")

    def test_readme_intro_contains_identity_role_and_location(self):
        intro = "\n".join(self.readme.splitlines()[:22]).lower()
        self.assertIn("jerry chong", intro)
        self.assertTrue(
            any(role in intro for role in ["enterprise architect", "solution architect", "architect"]),
            "README intro should describe Jerry Chong's architect role.",
        )
        self.assertIn("kuala lumpur", intro)
        self.assertIn("malaysia", intro)

    def test_readme_intro_contains_ai_and_cloud_positioning(self):
        intro = "\n".join(self.readme.splitlines()[:28]).lower()
        expected_signals = [
            "enterprise architecture",
            "cloud architecture",
            "ai architecture",
            "data architecture",
            "solution architecture",
            "multi-cloud",
        ]
        found = [signal for signal in expected_signals if signal in intro]
        self.assertGreaterEqual(
            len(found),
            5,
            "README intro should communicate current AI, cloud, and architecture positioning.",
        )

    def test_readme_contains_core_expertise_keywords(self):
        expected_keywords = [
            "cloud architecture",
            "enterprise architect",
            "solution architecture",
            "aws",
            "azure",
            "alibaba cloud",
            "alibaba cloud mvp",
            "terraform",
            "aviatrix",
            "fortinet",
            "ai",
            "data",
            "sap leanix",
        ]
        found = [keyword for keyword in expected_keywords if keyword in self.readme_lower]
        self.assertGreaterEqual(
            len(found),
            9,
            "README should contain enough expertise keywords to support traditional and AI search relevance.",
        )

    def test_readme_establishes_authority_and_entity_signals(self):
        authority_signals = [
            "jerry chong",
            "dhl",
            "alibaba cloud mvp",
            "tsinghua",
            "ex-cto",
            "ex-accenture",
            "kuala lumpur",
            "malaysia",
        ]
        found = [signal for signal in authority_signals if signal in self.readme_lower]
        self.assertGreaterEqual(
            len(found),
            8,
            "README should establish strong entity and authority signals for the Jerry Chong query.",
        )

    def test_readme_contains_owned_site_project_and_contact_signals(self):
        self.assertIn("https://jerrychong.xyz/", self.readme)
        self.assertIn("jerrychong25@gmail.com", self.readme)
        self.assertIn("mailto:jerrychong25@gmail.com", self.readme)
        self.assertIn("malaysia-map-data", self.readme)
        self.assertIn("awesome-malaysia", self.readme)

    def test_external_links_use_https(self):
        markdown_links = re.findall(r"\[[^\]]+\]\((https?://[^)]+)\)", self.readme)
        html_links = re.findall(r'href="(https?://[^"]+)"', self.readme, flags=re.IGNORECASE)
        urls = markdown_links + html_links
        self.assertGreater(len(urls), 0, "README should contain external identity and authority links.")
        insecure_urls = [url for url in urls if url.startswith("http://")]
        self.assertEqual(insecure_urls, [], f"Found insecure external links: {insecure_urls}")

    def test_all_html_images_have_non_empty_alt_text(self):
        img_tags = re.findall(r"<img\b[^>]*>", self.readme, flags=re.IGNORECASE)
        self.assertGreater(len(img_tags), 0, "README should contain image assets that can be validated.")
        missing_alt = []
        for tag in img_tags:
            match = re.search(r'alt="([^"]+)"', tag, flags=re.IGNORECASE)
            if not match or not match.group(1).strip():
                missing_alt.append(tag)
        self.assertEqual(missing_alt, [], f"Images missing alt text: {missing_alt}")

    def test_html_image_alt_text_mentions_jerry_chong_for_profile_badges(self):
        alt_texts = re.findall(r'<img\b[^>]*alt="([^"]+)"', self.readme, flags=re.IGNORECASE)
        profile_badge_alts = [alt.lower() for alt in alt_texts if "badge" in alt.lower() or "counter" in alt.lower()]
        self.assertTrue(profile_badge_alts, "README should include descriptive alt text for profile badges.")
        self.assertTrue(
            all("jerry chong" in alt for alt in profile_badge_alts),
            "Profile badge alt text should reinforce the Jerry Chong entity name.",
        )

    def test_markdown_images_have_non_empty_alt_text(self):
        markdown_images = re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", self.readme)
        self.assertGreater(len(markdown_images), 0, "README should contain at least one Markdown image.")
        blank_alt = [url for alt, url in markdown_images if not alt.strip()]
        self.assertEqual(blank_alt, [], f"Markdown images missing alt text: {blank_alt}")

    def test_header_links_use_centered_markdown_badges(self):
        self.assertIn("img.shields.io/badge/Official_Website", self.readme)
        self.assertIn("img.shields.io/badge/Portfolio_Website", self.readme)
        self.assertIn("img.shields.io/badge/LinkedIn", self.readme)
        self.assertIn("img.shields.io/badge/Email", self.readme)
        self.assertIn("| :-: | :-: | :-: | :-: |", self.readme)

    def test_sponsor_badge_uses_small_markdown_badge(self):
        self.assertIn("img.shields.io/badge/Buy%20Me%20a%20Coffee", self.readme)
        self.assertNotIn("cdn.buymeacoffee.com/buttons/v2/default-yellow.png", self.readme)

    def test_readme_has_multiple_identity_graph_links(self):
        identity_domains = [
            "linkedin.com",
            "twitter.com",
            "stackoverflow.com",
            "dev.to",
            "codepen.io",
            "kaggle.com",
            "hackerrank.com",
            "github.com",
            "jerrychong.xyz",
        ]
        found = [domain for domain in identity_domains if domain in self.readme_lower]
        self.assertGreaterEqual(
            len(found),
            6,
            "README should include multiple identity and authority links that help entity resolution.",
        )

    def test_metrics_svg_has_title_and_description(self):
        self.assertRegex(self.svg, r"<title>.*Jerry Chong.*</title>", "SVG should expose a descriptive title.")
        self.assertRegex(self.svg, r"<desc>.*GitHub metrics dashboard.*</desc>", "SVG should expose a descriptive summary.")

    def test_metrics_svg_contains_profile_name(self):
        self.assertIn("Jerry Chong", self.svg, "SVG should contain the profile name for semantic relevance.")

    def test_metrics_workflow_refreshes_profile_data_daily(self):
        self.assertIn('schedule: [{cron: "0 8 * * *"}]', self.workflow)
        self.assertIn("user: jerrychong25", self.workflow)
        self.assertIn("plugin_traffic: yes", self.workflow)


if __name__ == "__main__":
    unittest.main()
