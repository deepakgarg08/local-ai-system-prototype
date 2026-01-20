import inspect
import pipelines.query.retriever as retriever
import pipelines.prompting.assemble_prompt as prompting


def test_retriever_does_not_import_prompting():
    source = inspect.getsource(retriever)
    assert "assemble_prompt" not in source


def test_prompting_does_not_import_llms():
    source = inspect.getsource(prompting)
    forbidden = ["ollama", "openai", "BaseLLM"]
    for name in forbidden:
        assert name not in source


