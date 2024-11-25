from pathlib import Path


def get_artifact_file_path(file_name: str) -> str:
    artifacts_dir = Path(__file__).resolve().parent.parent.parent / "artifacts"

    artifacts_dir.mkdir(exist_ok=True)

    return artifacts_dir / file_name
