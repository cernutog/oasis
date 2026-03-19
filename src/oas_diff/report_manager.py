import os
import yaml
from .comparator import compare_specs
from .heuristic_engine import HeuristicEngine
from .generators.synthetic_generator import SyntheticDocxGenerator
from .generators.analytic_generator import AnalyticDocxGenerator
from .generators.impact_generator import ImpactDocxGenerator
from .resolver import resolve_spec
from .compatibility_analyzer import CompatibilityAnalyzer
from .generators.compatibility_generator import CompatibilityDocxGenerator

class OASDiffReportManager:
    """
    Orchestrates the comparison of two OAS files and the generation of reports.
    Handles loading files, running the diff, and dispatching to specialized generators.
    """

    def __init__(self, old_path, new_path, output_dir, preferences=None):
        self.old_path = old_path
        self.new_path = new_path
        self.output_dir = output_dir
        self.preferences = preferences or {}
        
        self.spec1 = self._load_spec(old_path)
        self.spec2 = self._load_spec(new_path)
        
        self.diff = None
        self.insights = None

    def _load_spec(self, path):
        """Loads an OAS file (YAML or JSON)."""
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def run_comparison(self):
        """Executes the core comparison logic."""
        debug = self.preferences.get('diff_debug_mode', False)
        self.diff = compare_specs(self.spec1, self.spec2, debug_mode=debug)
        
        engine = HeuristicEngine(self.diff)
        self.insights = engine.run()
        
        # Link insights back to the diff object for the generators
        self.diff.insights = self.insights
        return self.diff

    def generate_reports(self, report_types):
        """
        Generates requested reports.
        report_types: list of strings ('synthesis', 'analytical', 'impact')
        """
        if not self.diff:
            self.run_comparison()

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        results = []
        static_vars = self.preferences.get('diff_static_variables', {})

        # Report Dispatcher
        if 'synthesis' in report_types:
            path = os.path.join(self.output_dir, f"OAS_Comparison_Synthesis_{self._get_timestamp()}.docx")
            gen = SyntheticDocxGenerator(
                self.spec1, self.spec2, self.diff, 
                old_path=self.old_path, new_path=self.new_path,
                variables=static_vars,
                template_path=self.preferences.get('diff_template_synthesis')
            )
            gen.generate(path)
            results.append(path)

        if 'analytical' in report_types:
            path = os.path.join(self.output_dir, f"OAS_Comparison_Analytical_{self._get_timestamp()}.docx")
            gen = AnalyticDocxGenerator(
                self.spec1, self.spec2, self.diff, 
                old_path=self.old_path, new_path=self.new_path,
                variables=static_vars,
                template_path=self.preferences.get('diff_template_analytical')
            )
            gen.generate(path)
            results.append(path)

        if 'impact' in report_types:
            path = os.path.join(self.output_dir, f"OAS_Comparison_Impact_{self._get_timestamp()}.docx")
            gen = ImpactDocxGenerator(
                self.spec1, self.spec2, self.diff, 
                old_path=self.old_path, new_path=self.new_path,
                variables=static_vars,
                template_path=self.preferences.get('diff_template_impact')
            )
            gen.generate(path)
            results.append(path)

        if 'compatibility' in report_types:
            path = os.path.join(self.output_dir, f"OAS_Comparison_Interface_Compatibility_{self._get_timestamp()}.docx")
            # Resolve Specs First
            r1 = resolve_spec(self.spec1)
            r2 = resolve_spec(self.spec2)
            # Run Analyzer
            analyzer = CompatibilityAnalyzer(r1, r2)
            issues = analyzer.analyze()
            # Generate Report
            gen = CompatibilityDocxGenerator(
                issues, self.old_path, self.new_path, 
                template_path=self.preferences.get('diff_template_compatibility'),
                spec1=self.spec1, spec2=self.spec2
            )

            gen.generate(path)
            results.append(path)

        return results

    def _get_timestamp(self):
        import datetime
        return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
