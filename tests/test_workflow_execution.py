#!/usr/bin/env python3
"""
tests/test_workflow_execution.py
=================================
Unit tests for workflow execution without LLM calls.

Tests the core logic of execute_workflow and WorkflowExecutor
using mock tools to validate variable injection, step ordering,
and error handling.
"""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add repo root to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.tool_registry import registry, Tool
from core.workflow_executor import WorkflowExecutor
from core.agent.session_store import SessionStore


class MockTool(Tool):
    """Mock tool that returns predefined values without calling external services."""
    
    def __init__(self, name, description, params, output, result):
        self._name = name
        self._description = description
        self._params = params
        self._output = output
        self._result = result
    
    @property
    def name(self) -> str: return self._name
    @property
    def description(self) -> str: return self._description
    @property
    def category(self) -> str: return "mock"
    @property
    def params(self) -> dict: return self._params
    @property
    def output(self) -> dict: return self._output
    
    def execute(self, **kwargs):
        return {"result": self._result}


def test_variable_injection():
    """Test that execute_workflow correctly injects runtime variables."""
    print("\n🧪 Test 1: Variable Injection")
    
    # Create a mock workflow
    workflow = {
        "version": "1.0",
        "name": "test_workflow",
        "variables": {
            "input_docx": "path/to/document.docx",
            "input_rubric": "path/to/rubric.yaml",
            "output_dir": "path/to/output"
        },
        "steps": []
    }
    
    # Test execute_workflow tool
    tool = registry.get("execute_workflow")
    
    # Create temp files
    with tempfile.TemporaryDirectory() as tmpdir:
        workflow_path = Path(tmpdir) / "test_workflow.json"
        workflow_path.write_text(json.dumps(workflow))
        
        # Create a dummy document
        doc_path = Path(tmpdir) / "test.docx"
        doc_path.touch()
        
        # Create a dummy rubric
        rubric_path = Path(tmpdir) / "rubric.yaml"
        rubric_path.touch()
        
        output_dir = Path(tmpdir) / "output"
        
        # Test variable injection
        from core.tool_registry import WorkflowExecutorTool
        executor_tool = WorkflowExecutorTool()
        
        # Mock the WorkflowExecutor to avoid actual execution
        with patch('core.workflow_executor.WorkflowExecutor') as MockExecutor:
            mock_instance = MagicMock()
            mock_instance.execute.return_value = {"status": "completed", "log": []}
            MockExecutor.return_value = mock_instance
            
            # Execute with rubric_path
            result = executor_tool.execute(
                workflow_path=str(workflow_path),
                input_doc=str(doc_path),
                output_dir=str(output_dir),
                rubric_path=str(rubric_path)
            )
            
            # Verify variables were injected
            call_args = MockExecutor.call_args
            injected_workflow = call_args[0][0]
            
            assert injected_workflow["variables"]["input_docx"] == str(doc_path), \
                f"Expected {doc_path}, got {injected_workflow['variables']['input_docx']}"
            assert injected_workflow["variables"]["output_dir"] == str(output_dir), \
                f"Expected {output_dir}, got {injected_workflow['variables']['output_dir']}"
            assert injected_workflow["variables"]["input_rubric"] == str(rubric_path), \
                f"Expected {rubric_path}, got {injected_workflow['variables']['input_rubric']}"
            
            print("  ✅ Variables injected correctly")
            print(f"     input_docx: {injected_workflow['variables']['input_docx']}")
            print(f"     output_dir: {injected_workflow['variables']['output_dir']}")
            print(f"     input_rubric: {injected_workflow['variables']['input_rubric']}")


def test_workflow_executor_step_ordering():
    """Test that WorkflowExecutor runs steps in correct order."""
    print("\n🧪 Test 2: Step Ordering")
    
    execution_log = []
    
    def mock_execute(name, **kwargs):
        execution_log.append({"tool": name, "kwargs": kwargs})
        return {"result": {"status": "ok", "data": f"from_{name}"}}
    
    # Create a simple workflow
    workflow = {
        "version": "1.0",
        "name": "test_ordering",
        "variables": {
            "input_docx": "/tmp/test.docx",
            "input_rubric": "/tmp/rubric.yaml",
            "output_dir": "/tmp/output"
        },
        "steps": [
            {
                "id": "step_1",
                "tool": "docx_extract",
                "params": {"input": "${input_docx}", "output_dir": "${output_dir}/extracted"},
                "output": {"contents_md": "contents.md"},
                "on_error": "abort"
            },
            {
                "id": "step_2",
                "tool": "grader",
                "params": {"scores": "${step_1.result.contents_md}", "config": "${input_rubric}"},
                "output": {"final_grade": "grade"},
                "on_error": "abort"
            }
        ]
    }
    
    # Mock registry.execute
    with patch('core.tool_registry.registry.execute', side_effect=mock_execute):
        executor = WorkflowExecutor(workflow)
        result = executor.execute()
        
        assert result["status"] == "completed", f"Expected completed, got {result['status']}"
        assert len(execution_log) == 2, f"Expected 2 steps, got {len(execution_log)}"
        assert execution_log[0]["tool"] == "docx_extract", "First step should be docx_extract"
        assert execution_log[1]["tool"] == "grader", "Second step should be grader"
        
        print("  ✅ Steps executed in correct order")
        print(f"     Step 1: {execution_log[0]['tool']}")
        print(f"     Step 2: {execution_log[1]['tool']}")


def test_error_handling_skip():
    """Test that on_error: skip continues workflow after failure."""
    print("\n🧪 Test 3: Error Handling (skip)")
    
    execution_log = []
    
    def mock_execute(name, **kwargs):
        execution_log.append({"tool": name})
        if name == "failing_tool":
            raise RuntimeError("Simulated failure")
        return {"result": {"status": "ok"}}
    
    workflow = {
        "version": "1.0",
        "name": "test_skip",
        "variables": {"test_var": "value"},
        "steps": [
            {
                "id": "step_1",
                "tool": "docx_extract",
                "params": {},
                "output": {"data": "data1"},
                "on_error": "abort"
            },
            {
                "id": "step_2",
                "tool": "failing_tool",
                "params": {},
                "output": {"data": "data2"},
                "on_error": "skip"
            },
            {
                "id": "step_3",
                "tool": "grader",
                "params": {},
                "output": {"data": "data3"},
                "on_error": "abort"
            }
        ]
    }
    
    with patch('core.tool_registry.registry.execute', side_effect=mock_execute):
        executor = WorkflowExecutor(workflow)
        result = executor.execute()
        
        assert result["status"] == "completed", f"Expected completed, got {result['status']}"
        assert len(execution_log) == 3, f"Expected 3 steps, got {len(execution_log)}"
        
        # Check that step_2 was attempted but skipped
        step_2_log = [log for log in result["log"] if log["step"] == "step_2"]
        assert len(step_2_log) == 1, "Step 2 should be in log"
        assert step_2_log[0]["status"] == "skipped", f"Step 2 should be skipped, got {step_2_log[0]['status']}"
        
        print("  ✅ Error handling works correctly")
        print(f"     Step 1: {execution_log[0]['tool']} (success)")
        print(f"     Step 2: {execution_log[1]['tool']} (failed, skipped)")
        print(f"     Step 3: {execution_log[2]['tool']} (success)")


def test_session_management():
    """Test that SessionStore correctly saves and loads sessions."""
    print("\n🧪 Test 4: Session Management")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        store = SessionStore(store_dir=tmpdir)
        
        # Test save and load
        session_id = "test_session_123"
        messages = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"}
        ]
        
        store.save(session_id, messages)
        loaded = store.load(session_id)
        
        assert len(loaded) == 2, f"Expected 2 messages, got {len(loaded)}"
        assert loaded[0]["role"] == "user", "First message should be user"
        assert loaded[1]["role"] == "assistant", "Second message should be assistant"
        
        # Test list sessions
        sessions = store.list_sessions()
        assert session_id in sessions, f"Expected {session_id} in sessions"
        
        # Test delete
        store.delete(session_id)
        assert store.load(session_id) == [], "Session should be empty after delete"
        
        print("  ✅ Session management works correctly")
        print(f"     Saved and loaded session: {session_id}")
        print(f"     Messages: {len(loaded)}")


def test_rubric_inference():
    """Test that execute_workflow can infer rubric path from metadata."""
    print("\n🧪 Test 5: Rubric Path Inference")
    
    workflow = {
        "version": "1.0",
        "name": "test_inference",
        "metadata": {
            "rubric_id": "hito2"
        },
        "variables": {
            "input_docx": "path/to/document.docx",
            "input_rubric": "path/to/rubric.yaml",
            "output_dir": "path/to/output"
        },
        "steps": []
    }
    
    with tempfile.TemporaryDirectory() as tmpdir:
        workflow_path = Path(tmpdir) / "test_workflow.json"
        workflow_path.write_text(json.dumps(workflow))
        
        doc_path = Path(tmpdir) / "test.docx"
        doc_path.touch()
        
        output_dir = Path(tmpdir) / "output"
        
        # Create a mock rubric file
        rubric_path = Path(tmpdir) / "configs" / "rubric_hito2.yaml"
        rubric_path.parent.mkdir(parents=True, exist_ok=True)
        rubric_path.touch()
        
        # Temporarily change to tmpdir to test relative path inference
        import os
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        
        try:
            from core.tool_registry import WorkflowExecutorTool
            executor_tool = WorkflowExecutorTool()
            
            with patch('core.workflow_executor.WorkflowExecutor') as MockExecutor:
                mock_instance = MagicMock()
                mock_instance.execute.return_value = {"status": "completed", "log": []}
                MockExecutor.return_value = mock_instance
                
                # Execute without rubric_path (should infer from metadata)
                result = executor_tool.execute(
                    workflow_path=str(workflow_path),
                    input_doc=str(doc_path),
                    output_dir=str(output_dir)
                    # No rubric_path provided
                )
                
                call_args = MockExecutor.call_args
                injected_workflow = call_args[0][0]
                
                # Check that rubric was inferred
                expected_rubric = f"configs/rubric_hito2.yaml"
                assert injected_workflow["variables"]["input_rubric"] == expected_rubric, \
                    f"Expected {expected_rubric}, got {injected_workflow['variables']['input_rubric']}"
                
                print("  ✅ Rubric path inferred correctly from metadata")
                print(f"     Inferred: {injected_workflow['variables']['input_rubric']}")
        finally:
            os.chdir(original_cwd)


def main():
    """Run all tests."""
    print("=" * 60)
    print("🧪 Workflow Execution Tests (No LLM)")
    print("=" * 60)
    
    try:
        test_variable_injection()
        test_workflow_executor_step_ordering()
        test_error_handling_skip()
        test_session_management()
        test_rubric_inference()
        
        print("\n" + "=" * 60)
        print("✅ All 5 tests passed!")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
