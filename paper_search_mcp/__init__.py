from .config import load_env_file

load_env_file()



def _raise_pypdf_stream_budget() -> None:
    """Raise pypdf's per-stream parsing budget.

    pypdf >= 6.21 enforces a 2,000,000-token budget per content stream as a
    DoS guard; some legitimate scientific PDFs exceed it and text extraction
    fails with "Reached maximum number of tokens per stream". Keep the guard,
    raise the ceiling 10x. The configuration is context-scoped: it applies to
    this import context and every context derived from it (threads keep the
    default).
    """
    from pypdf import Configuration, overwrite_configuration

    overwrite_configuration(
        Configuration(stream_parsing_work_maximum_count=20_000_000)
    )


_raise_pypdf_stream_budget()
