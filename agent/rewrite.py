import textwrap
import os
import subprocess
import re

from agent.model import JDKModernizerModel


class JavaRewrite:
    def __init__(self, project_path: str, model: JDKModernizerModel):
        self.project_path = project_path
        self.model = model
        self.files_to_modernize = []

    def modernize_project_infra(self):
        """
        Prepares the project infrastructure for modernization.
        Updates the pom.xml to Java 25 and injects the compiler plugin configuration.
        """
        print(f"Preparing project infrastructure at: {self.project_path}")
        pom_path = os.path.join(self.project_path, "pom.xml")

        if not os.path.exists(pom_path):
            print(f"pom.xml not found. Skipping infra modernization.")
            return
        try:
            with open(pom_path, "r", encoding="utf-8") as file:
                content = file.read()

            # 1. Update/Add properties
            # If the tag exists, update to 25.
            for tag in [
                "maven.compiler.source",
                "maven.compiler.target",
                "java.version",
                "maven.compiler.release",
            ]:
                content = re.sub(f"<{tag}>.*?</{tag}>", f"<{tag}>25</{tag}>", content)

            # Ensure release 25 exists (crucial for switch on Object)
            if "<maven.compiler.release>" not in content:
                content = content.replace(
                    "</properties>",
                    "    <maven.compiler.release>25</maven.compiler.release>\n    </properties>",
                )
            # 2. Define the clean Build Section
            # This ensures the compiler plugin is configured for Java 25 features.
            compiler_build_section = textwrap.dedent(
                """\
                    <build>
                        <plugins>
                            <plugin>
                                <groupId>org.apache.maven.plugins</groupId>
                                <artifactId>maven-compiler-plugin</artifactId>
                                <version>3.14.1</version>
                                <configuration>
                                    <release>25</release>
                                    <compilerArgs>
                                        <arg>--enable-preview</arg>
                                    </compilerArgs>
                                </configuration>
                            </plugin>
                            <plugin>
                                <groupId>org.openrewrite.maven</groupId>
                                <artifactId>rewrite-maven-plugin</artifactId>
                                <version>6.2.0</version>
                                <configuration>
                                    <activeRecipes>
                                        <recipe>org.openrewrite.java.migrate.UpgradeToJava21</recipe>
                                        <recipe>org.openrewrite.java.format.AutoFormat</recipe>
                                    </activeRecipes>
                                </configuration>
                                <dependencies>
                                    <dependency>
                                        <groupId>org.openrewrite.recipe</groupId>
                                        <artifactId>rewrite-migrate-java</artifactId>
                                        <version>3.2.0</version>
                                    </dependency>
                                </dependencies>
                            </plugin>
                        </plugins>
                    </build>
                """
            )

            # 3. Remove any existing <build> block to prevent nesting/duplicates
            content = re.sub(r"\s*<build>.*?</build>", "", content, flags=re.DOTALL)

            content = re.sub(r"\n{3,}", "\n\n", content)
            indented_build = textwrap.indent(compiler_build_section, "    ")
            content = content.strip().replace("</project>", "")
            final_pom = f"{content}\n\n{indented_build}\n</project>"

            with open(pom_path, "w", encoding="utf-8") as file:
                file.write(final_pom)

            # Beautify pom.xml after each file modernization
            self.format_pom()

            print("pom.xml file successfully upgraded to Java 25.")
        except Exception as e:
            print(f"Error updating pom.xml: {e}")

    def process_file(self, file_path: str):
        """
        Processes a single Java file for modernization.
        """
        file_name = os.path.basename(file_path)
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                legacy_code = file.read()

            modernized_code = self.model.get_modernization_suggestion(
                file_name, legacy_code
            )

            with open(file_path, "w", encoding="utf-8") as file:
                file.write(modernized_code)

            print(f"Successfully modernized file: {file_path}")
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

    def apply_openrewrite(self):
        """
        Applies OpenRewrite recipes to the project.
        """
        print(f"Running OpenRewrite recipes on project at: {self.project_path}")
        try:
            result = subprocess.run(
                ["mvn", "rewrite:run"],
                cwd=self.project_path,
                # capture_output=True,
                text=True,
                check=True,
            )
            if result.returncode == 0:
                print("OpenRewrite recipes applied successfully.")
            else:
                print("OpenRewrite execution failed with the following errors:")
                print(result.stderr)
        except Exception as e:
            print(f"Error running OpenRewrite: {e}")

    def format_pom(self):
        """Uses OpenRewrite to fix the messy indentation in pom.xml."""
        print("🧹 Beautifying pom.xml...")
        cmd = [
            "mvn",
            "org.openrewrite.maven:rewrite-maven-plugin:run",
            "-Drewrite.activeRecipes=org.openrewrite.xml.format.NormalizeFormat",
            "-q",
        ]
        subprocess.run(cmd, cwd=self.project_path)

    def verify_project_by_compiling(self):
        """
        Verifies if the provided project is valid by compiling it using Maven.
        Runs `mvn compile` to check syntax errors.
        """
        print(f"Verifying project at: {self.project_path} by compiling with Maven")
        try:
            result = subprocess.run(
                ["mvn", "clean", "compile", "-q"],
                cwd=self.output_path,
                capture_output=True,
                text=True,
                check=True,
            )
            if result.returncode == 0:
                print("Project compiled successfully. No syntax errors found.")
                return True
            else:
                print("Compilation failed with the following errors:")
                print(result.stderr)
                return False
        except Exception as e:
            print(f"An error occurred while compiling the project: {e}")
            return False, str(e)
