"""
Comprehensive stress tests for text overflow protection, auto-wrapping,
and collision-free layout across all Pixel Readme Kit SVG generators.
"""

import unittest
import xml.etree.ElementTree as ET
from generator.engine import (
    measure_mono_text_width,
    clamp_text_to_width,
    wrap_text_to_lines,
    generate_header,
    _generate_compact_header,
    generate_callout,
    generate_footer,
    generate_frame,
    generate_chip,
    generate_divider,
    generate_splitter,
    generate_metrics,
    generate_progress,
    generate_techstack,
    generate_timeline,
    generate_social,
    generate_starchart,
    generate_profile_card,
)


class TestTextOverflowRobustness(unittest.TestCase):
    """Verifies that all components handle extreme text gracefully without crashing or invalid XML."""

    def assert_valid_svg(self, svg_str):
        """Helper to verify strict XML validity and basic SVG structure."""
        self.assertIsInstance(svg_str, str)
        self.assertTrue(svg_str.startswith("<svg"))
        self.assertTrue(svg_str.endswith("</svg>"))
        try:
            root = ET.fromstring(svg_str)
            self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")
        except ET.ParseError as e:
            self.fail(f"Invalid XML generated: {e}\nSnippet: {svg_str[:300]}")

    # -------------------------------------------------------------------------
    # 1. Typography & Layout Helper Unit Tests
    # -------------------------------------------------------------------------

    def test_measure_mono_text_width(self):
        w_empty = measure_mono_text_width("")
        self.assertEqual(w_empty, 0)

        w_ascii = measure_mono_text_width("HELLO", font_size=10)
        self.assertAlmostEqual(w_ascii, 5 * 6.1, places=1)

        # Unicode special glyphs should have larger measured width
        w_glyph = measure_mono_text_width("★", font_size=10)
        self.assertGreater(w_glyph, 6.1)

    def test_clamp_text_to_width(self):
        # Text that fits should be returned unchanged
        short_text = "ABC"
        self.assertEqual(clamp_text_to_width(short_text, 100, font_size=10), short_text)

        # Text that exceeds max_width should be truncated with suffix
        long_text = "A" * 100
        clamped = clamp_text_to_width(long_text, 50, font_size=10, suffix="...")
        self.assertTrue(clamped.endswith("..."))
        self.assertLess(measure_mono_text_width(clamped, font_size=10), 55)

        # Extreme narrow width
        clamped_narrow = clamp_text_to_width(long_text, 5, font_size=10)
        self.assertTrue(len(clamped_narrow) <= 3)

    def test_wrap_text_to_lines(self):
        sample = "Building high-performance runtimes and resilient developer tooling across edge networks."
        lines = wrap_text_to_lines(sample, max_width=200, font_size=11, max_lines=2)
        self.assertTrue(1 <= len(lines) <= 2)
        for line in lines:
            self.assertLessEqual(measure_mono_text_width(line, font_size=11), 220)

        # Continuous string without spaces
        no_spaces = "A" * 150
        lines_no_spaces = wrap_text_to_lines(no_spaces, max_width=100, font_size=11, max_lines=2)
        self.assertTrue(1 <= len(lines_no_spaces) <= 2)
        self.assertTrue(lines_no_spaces[-1].endswith("..."))

    # -------------------------------------------------------------------------
    # 2. Star Growth Trend Chart (generate_starchart)
    # -------------------------------------------------------------------------

    def test_starchart_extreme_text(self):
        long_title = "COMPREHENSIVE MULTI-REGION TELEMETRY TRAJECTORY WITH DEEP AUDIT METRICS"
        long_repo = "extremely-long-organization-name/nested-monorepo-service-system"
        extreme_stars = "999,999,999 STARS"
        extreme_delta = "+5,432,100% IN 30 DAYS"

        for style in ["cyberpunk", "tactical", "minimal"]:
            svg = generate_starchart(
                style=style,
                title=long_title,
                repo=long_repo,
                current=extreme_stars,
                delta=extreme_delta,
                points=[10, 50, 200, 1500, 8000, 25000, 99999],
            )
            self.assert_valid_svg(svg)
            # Ensure title doesn't spill over or produce invalid SVG tags
            self.assertIn("★", svg)

    def test_starchart_no_title_repo_collision(self):
        """Verifies that in starchart, title and repo do not share the same starting coordinates or overlap."""
        title = "OPEN SOURCE TRAJECTORY // TELEMETRY"
        repo = "kazinagg/pixel-readme-kit"
        svg = generate_starchart(title=title, repo=repo)
        self.assert_valid_svg(svg)

        # Confirm hardcoded x=230 collision was removed
        self.assertNotIn('x="230">// kazinagg/pixel-readme-kit', svg)
        # Check repo text exists with dynamic x > 250
        root = ET.fromstring(svg)
        texts = root.findall(".//{http://www.w3.org/2000/svg}text")
        repo_nodes = [t for t in texts if "kazinagg/pixel-readme-kit" in (t.text or "")]
        if repo_nodes:
            self.assertGreater(float(repo_nodes[0].attrib.get("x", "0")), 250)

    # -------------------------------------------------------------------------
    # 3. Headers (generate_header & _generate_compact_header)
    # -------------------------------------------------------------------------

    def test_header_extreme_strings(self):
        long_title = "SYSTEM INITIALIZATION OVERRIDE PROTOCOL"
        long_sub = "Continuous deployment pipelines processing terabytes of sensor telemetry across geo-distributed compute clusters."
        long_specs = [
            ("DEPLOYMENT_CLUSTER", "K8S_ENTERPRISE_PRODUCTION_US_EAST_1A"),
            ("LATENCY_TARGET_P99", "SUB_MILLISECOND_ZERO_JITTER"),
            ("STATUS_DIAGNOSTIC", "ALL_SUBSYSTEMS_NOMINAL_LEVEL_99"),
        ]

        for style in ["cyberpunk", "tactical", "minimal"]:
            # Full header
            svg_full = generate_header(
                style=style,
                title=long_title,
                subtitle=long_sub,
                specs=long_specs,
            )
            self.assert_valid_svg(svg_full)

            # Compact header
            svg_compact = generate_header(
                style=style,
                title=long_title,
                subtitle=long_sub,
                compact=True,
            )
            self.assert_valid_svg(svg_compact)

    # -------------------------------------------------------------------------
    # 4. Callout / Quote Blocks (generate_callout)
    # -------------------------------------------------------------------------

    def test_callout_extreme_strings(self):
        long_type = "CRITICAL_SECURITY_AUDIT_WARNING"
        long_title = "ZERO-DAY VULNERABILITY MITIGATION ADVISORY NOTICE"
        long_sub = "Immediate architectural patch required. Please follow cryptographic hygiene protocols across all connected edge nodes immediately."

        for style in ["cyberpunk", "tactical", "minimal"]:
            # Standard Callout
            svg_std = generate_callout(
                style=style,
                callout_type=long_type,
                title=long_title,
                subtitle=long_sub,
                is_quote=False,
            )
            self.assert_valid_svg(svg_std)

            # Markdown Quote Mode
            svg_quote = generate_callout(
                style=style,
                callout_type=long_type,
                title=long_title,
                subtitle=long_sub,
                is_quote=True,
            )
            self.assert_valid_svg(svg_quote)

    # -------------------------------------------------------------------------
    # 5. Footer & Frame Blocks
    # -------------------------------------------------------------------------

    def test_footer_extreme_strings(self):
        long_stat = "ALL_MICROSERVICES_REPORTING_HEALTHY_AND_LOAD_BALANCED"
        long_tele = "GPU_UTIL: 99.4% // TEMP: 42C // MEMORY_ALLOC: 128GB/128GB // LATENCY: 0.2ms"

        for style in ["cyberpunk", "tactical", "minimal"]:
            svg = generate_footer(
                style=style,
                status=long_stat,
                sub_text=long_tele,
            )
            self.assert_valid_svg(svg)

    def test_frame_extreme_strings(self):
        long_title = "SECURITY_ZONE_RESTRICTED_ACCESS_PERIMETER"
        long_tag = "ENC_SHA512_AUTHENTICATED_SECURE_CHANNEL"

        for style in ["cyberpunk", "tactical", "minimal"]:
            svg_top = generate_frame(
                style=style,
                title=long_title,
                tag=long_tag,
                frame_type="top",
            )
            self.assert_valid_svg(svg_top)

            svg_bot = generate_frame(
                style=style,
                title=long_title,
                tag=long_tag,
                frame_type="bottom",
            )
            self.assert_valid_svg(svg_bot)

    # -------------------------------------------------------------------------
    # 6. Data Widgets: Metrics, Progress, TechStack, Timeline
    # -------------------------------------------------------------------------

    def test_metrics_extreme_strings(self):
        cards = [
            {"label": "AGGREGATE_SYSTEM_THROUGHPUT_PER_SECOND", "value": "128,450,000 OPS", "delta": "+450.2% YOY", "status": "OVERCLOCKED"},
            {"label": "ACTIVE_DISTRIBUTED_SHARDS", "value": "65,536 SHARDS", "delta": "+100% HEALTH", "status": "MAX_CAPACITY"},
            {"label": "GLOBAL_CACHE_HIT_RATE", "value": "99.9999%", "delta": "STABLE", "status": "OPTIMAL"},
            {"label": "MEAN_TIME_TO_RECOVERY", "value": "0.0004 MS", "delta": "-99.8%", "status": "CRITICAL_LOW"},
        ]

        for count in [1, 2, 3, 4]:
            svg = generate_metrics(cards=cards[:count], style="cyberpunk")
            self.assert_valid_svg(svg)

    def test_progress_extreme_strings(self):
        long_lbl = "NEURAL_NET_TRAINING_EPOCH_99999_CHECKPOINT_SERIALIZATION"
        long_sub = "BATCH: 1048576/1048576 // LOSS: 0.0000012 // GRADIENT_NORM: 0.001 // GPU_POWER: 450W"

        for pct in [0, 42, 99, 100]:
            svg = generate_progress(
                label=long_lbl,
                value=pct,
                sub=long_sub,
                style="tactical",
            )
            self.assert_valid_svg(svg)

    def test_techstack_extreme_strings(self):
        items = [
            ("TYPESCRIPT_ENTERPRISE_APPLICATION", "CORE_LANGUAGE"),
            ("KUBERNETES_CONTAINER_ORCHESTRATION", "CLOUD_INFRA"),
            ("POSTGRESQL_DISTRIBUTED_CITUS_CLUSTER", "PRIMARY_DATA"),
            ("APACHE_KAFKA_STREAMING_PLATFORM", "EVENT_PIPELINE"),
            ("RUST_SYSTEMS_PERFORMANCE_ENGINE", "HARDWARE_LEVEL"),
        ]

        svg = generate_techstack(items=items, columns=5, style="minimal")
        self.assert_valid_svg(svg)

    def test_timeline_extreme_strings(self):
        milestones = [
            {
                "date": "2026-Q1-GLOBAL-LTS-DEPLOYMENT",
                "title": "DISTRIBUTED CONSENSUS ENGINE VALIDATION PHASE",
                "desc": "Benchmarked raft state machine under artificial network partitions with 10M synthetic client connections.",
                "status": "COMPLETED",
            },
            {
                "date": "2026-Q2-HARDENING-RELEASE",
                "title": "CRYPTOGRAPHIC ZERO-KNOWLEDGE PROOF INTEGRATION",
                "desc": "Rolled out zk-SNARK verifier contract across decentralized nodes.",
                "status": "IN_PROGRESS",
            },
        ]

        svg = generate_timeline(milestones=milestones, style="cyberpunk")
        self.assert_valid_svg(svg)

    # -------------------------------------------------------------------------
    # 7. Social & Profile Card
    # -------------------------------------------------------------------------

    def test_social_extreme_strings(self):
        long_title = "NEXT_GEN_PIXEL_FRAMEWORK_FOR_ENGINEERS"
        long_repo = "enterprise-architecture-group/high-velocity-systems"
        long_sub = "Empowering high-performance engineering teams with telemetry-ready visual identity widgets and status dashboards."
        tags = ["KUBERNETES", "DISTRIBUTED_SYSTEMS", "WEBGPU", "TYPESCRIPT", "HIGH_THROUGHPUT", "RESILIENT_STORAGE"]

        svg = generate_social(
            title=long_title,
            repo=long_repo,
            subtitle=long_sub,
            tags=tags,
            style="tactical",
        )
        self.assert_valid_svg(svg)

    def test_profile_card_extreme_strings(self):
        long_name = "ALEXANDER VON SCHWEINFURT-DEV"
        long_role = "PRINCIPAL SYSTEMS ARCHITECT & HIGH-PERFORMANCE RUNTIME ENGINEER"
        long_bio = "Architecting fault-tolerant microservices, zero-alloc runtimes, and developer observability kits across continents."
        long_loc = "GLOBAL REMOTE // UTC+09 // TOKYO & BERLIN"
        long_status = "ACTIVELY CONSULTING FOR SERIES-B+"
        long_badge = "RANK_ELITE_S_TIER"

        for style in ["cyberpunk", "tactical", "minimal"]:
            svg = generate_profile_card(
                style=style,
                name=long_name,
                role=long_role,
                bio=long_bio,
                location=long_loc,
                status=long_status,
                badge=long_badge,
            )
            self.assert_valid_svg(svg)

    # -------------------------------------------------------------------------
    # 8. Chips, Dividers & Splitters
    # -------------------------------------------------------------------------

    def test_chip_and_splitter_extreme_strings(self):
        long_chip = "VERY_LONG_ENTERPRISE_PIPELINE_STATUS_LABEL"
        svg_chip = generate_chip(text=long_chip, width=150, style="cyberpunk")
        self.assert_valid_svg(svg_chip)

        long_splitter = "[MODULE: HIGH_FREQUENCY_ORDER_MATCHING_ENGINE_CLUSTER_v5]"
        for style in ["cyberpunk", "tactical", "minimal"]:
            svg_splitter = generate_splitter(label=long_splitter, style=style)
            self.assert_valid_svg(svg_splitter)

        svg_div = generate_divider(style="cyberpunk")
        self.assert_valid_svg(svg_div)


if __name__ == "__main__":
    unittest.main()
