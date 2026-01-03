"""
Viewer Module Tests.

Tests for the documentation viewer (redoc_gen.py, doc_viewer.py).
"""

import pytest
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


class TestRedocGenerator:
    """
    Test suite for the Redoc HTML generator.
    """
    
    def test_redoc_gen_import(self):
        """Verify redoc_gen module can be imported."""
        from src import redoc_gen
        assert hasattr(redoc_gen, 'RedocGenerator'), "RedocGenerator class should exist"
    
    def test_redoc_generator_initialization(self):
        """Verify RedocGenerator can be instantiated."""
        from src.redoc_gen import RedocGenerator
        
        gen = RedocGenerator()
        assert gen is not None
    
    def test_redoc_generator_has_required_methods(self):
        """Verify RedocGenerator has required methods."""
        from src.redoc_gen import RedocGenerator
        
        gen = RedocGenerator()
        assert hasattr(gen, 'get_html_content'), "Should have get_html_content method"
    
    def test_redoc_generates_valid_html(self, generate_oas):
        """Test that Redoc generates valid HTML from OAS."""
        from src.redoc_gen import RedocGenerator
        import yaml
        
        # Generate OAS
        output_dir = generate_oas(gen_30=False, gen_31=True, gen_swift=False)
        oas_files = [f for f in output_dir.glob("*3.1*.yaml") if "SWIFT" not in f.name]
        
        if not oas_files:
            pytest.skip("No OAS file generated")
        
        with open(oas_files[0], 'r', encoding='utf-8') as f:
            oas_content = f.read()
        
        gen = RedocGenerator()
        html = gen.get_html_content(oas_content)
        
        # Verify HTML structure
        assert '<!DOCTYPE html>' in html, "Should be valid HTML document"
        assert '<html>' in html or '<html ' in html, "Should have html tag"
        assert 'redoc' in html.lower(), "Should contain Redoc"
    
    def test_redoc_html_has_toolbar(self, generate_oas):
        """Test that generated HTML has the custom toolbar."""
        from src.redoc_gen import RedocGenerator
        
        output_dir = generate_oas(gen_30=False, gen_31=True, gen_swift=False)
        oas_files = [f for f in output_dir.glob("*3.1*.yaml") if "SWIFT" not in f.name]
        
        with open(oas_files[0], 'r', encoding='utf-8') as f:
            oas_content = f.read()
        
        gen = RedocGenerator()
        html = gen.get_html_content(oas_content)
        
        # Check for toolbar elements
        assert 'doc-toolbar' in html, "Should have toolbar div"
        assert 'Save HTML' in html, "Should have Save HTML button"
        assert 'Print' in html, "Should have Print button"
    
    def test_redoc_html_has_download_filename(self, generate_oas):
        """Test that generated HTML uses correct download filename."""
        from src.redoc_gen import RedocGenerator
        
        output_dir = generate_oas(gen_30=False, gen_31=True, gen_swift=False)
        oas_files = [f for f in output_dir.glob("*3.1*.yaml") if "SWIFT" not in f.name]
        
        with open(oas_files[0], 'r', encoding='utf-8') as f:
            oas_content = f.read()
        
        gen = RedocGenerator()
        html = gen.get_html_content(oas_content)
        
        # Check that HTML is generated with title
        assert 'API Documentation' in html, "Should contain API Documentation title"


class TestDocViewer:
    """
    Test suite for the docked documentation viewer.
    """
    
    def test_doc_viewer_import(self):
        """Verify doc_viewer module can be imported."""
        from src import doc_viewer
        assert hasattr(doc_viewer, 'DockedDocViewer'), "DockedDocViewer class should exist"
    
    def test_doc_viewer_has_api_class(self):
        """Verify DocViewerAPI class exists."""
        from src.doc_viewer import DocViewerAPI
        assert DocViewerAPI is not None
    
    def test_doc_viewer_api_methods(self):
        """Verify DocViewerAPI has required methods."""
        from src.doc_viewer import DocViewerAPI
        from multiprocessing import Value
        import ctypes
        
        snap_flag = Value(ctypes.c_int, 1)
        api = DocViewerAPI(snap_flag)
        
        assert hasattr(api, 'toggle_snap'), "Should have toggle_snap method"
        assert hasattr(api, 'get_snap_state'), "Should have get_snap_state method"
        assert hasattr(api, 'sync_editor'), "Should have sync_editor method"
    
    def test_doc_viewer_api_snap_toggle(self):
        """Test snap state toggling."""
        from src.doc_viewer import DocViewerAPI
        from multiprocessing import Value
        import ctypes
        
        snap_flag = Value(ctypes.c_int, 1)  # Start snapped
        api = DocViewerAPI(snap_flag)
        
        # Initial state should be True (snapped)
        assert api.get_snap_state() == True
        
        # Toggle should return new state
        new_state = api.toggle_snap()
        assert new_state == False
        assert api.get_snap_state() == False
        
        # Toggle again
        new_state = api.toggle_snap()
        assert new_state == True
