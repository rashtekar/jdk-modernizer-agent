import os
import shutil
from agent.scanner import scan_java_project
from agent.model import JDKModernizerModel
import subprocess
from agent.rewrite import JavaRewrite


class JDKModernizerAgent:
    def __init__(self, legacy_path: str, output_path: str):
        self.legacy_path = legacy_path
        self.output_path = output_path
        self.model = JDKModernizerModel()
        self.rewrite = JavaRewrite(self.output_path, self.model)

    def prepare_workspace(self):
        """
        Prepares the workspace by copying the legacy project to the output path.
        """
        print(
            f"Preparing workspace by copying from {self.legacy_path} to {self.output_path}"
        )
        # 1. Clear the output directory if it exists to start fresh
        if os.path.exists(self.output_path):
            shutil.rmtree(self.output_path)

        # 2. Copy the entire tree
        shutil.copytree(self.legacy_path, self.output_path)

        print(f"Workspace prepared at: {self.output_path}")

    def start_modernization(self):
        """
        Starts the modernization process by scanning the project, reading files, and getting suggestions from the model.
        """
        # Step 0: Prepare workspace
        self.prepare_workspace()

        # Step 1: Prepare project for modernization
        self.rewrite.modernize_project_infra()

        # Step 2: Scan the project for Java files
        print(f"Scanning project at: {self.output_path}")
        self.files_to_modernize = scan_java_project(self.output_path)

        # Step 3: Call LLM to get modernization suggestions
        for file_path in self.files_to_modernize:
            self.rewrite.process_file(file_path)

        # Step 4: Call OpenRewrite again to finalize modernization
        self.rewrite.apply_openrewrite()

        # Step 5: Verify the modernization code
        success = self.rewrite.verify_project_by_compiling()
        if not success:
            print(f" Modernization introduced compilation errors and broke the code.")


if __name__ == "__main__":
    project_path = "./samples/legacy-app"
    output_path = "./samples/modernized-app"
    agent = JDKModernizerAgent(project_path, output_path)

    agent.start_modernization()
