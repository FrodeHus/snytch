import base64
import os
import tarfile, re
from typing import IO, List, Tuple
from ludvig.types import Finding, FindingSample, Image, Layer, SecretFinding, Severity, YaraRuleMatch
import yara


class ImageScanner:
    def __init__(self, image: Image, yara_rules: yara.Rules, severity_level : Severity = Severity.MEDIUM) -> None:
        self.image = image
        self.yara = yara_rules
        self.severity_level = severity_level
        self.findings: List[Finding] = []

    def scan(self):
        for layer in [l for l in self.image.layers if not l.empty_layer]:
            with self.image.image_archive.extractfile(
                "{}/layer.tar".format(layer.id)
            ) as layer_archive:

                with tarfile.open(fileobj=layer_archive, mode="r") as lf:
                    for member in lf.getmembers():
                        if os.path.basename(member.name).startswith(".wh."):
                            self.__whiteout(member.name, layer)

                        for _, finding in enumerate(
                            self.__scan_files(lf, member, layer)
                        ):
                            if finding:
                                self.findings.append(finding)

    def __whiteout(self, filename: str, layer: Layer):
        finding = [
            finding
            for finding in self.findings
            if finding.filename == filename.replace(".wh.", "")
        ]

        for f in finding:
            f.whiteout = True
            f.removed_by = layer.created_by

    def __extract_file(
        self, image: tarfile.TarFile, file: tarfile.TarInfo
    ) -> IO[bytes]:
        if file.isfile():
            return image.extractfile(file)
        return None

    def __scan_environment(self, variables: List[str]) -> Finding:
        pass

    def __scan_files(
        self, image: tarfile.TarFile, file: tarfile.TarInfo, layer: Layer = None
    ) -> Finding:
        data = self.__extract_file(image, file)
        if not data:
            return None
        try:
            matches = self.yara.match(data=data.read())
            for match in matches:
                
                severity = Severity[match.meta["severity"]] if "severity" in match.meta else Severity.UNKNOWN
                if severity < self.severity_level:
                    continue
                samples = FindingSample.from_yara_match(match)
                yield SecretFinding(YaraRuleMatch(match), samples, file.name, layer)
        except Exception as ex:
            return print(ex)
        finally:
            data.close()
            
    def __decode_content(self, content: str) -> str:
        for match in self.__possible_base64_encoding(content):
            try:
                decoded = base64.b64decode(match.group()).decode("utf-8")
                content = content.replace(match.group(), decoded)
            except UnicodeDecodeError:
                continue
        return content

    def __possible_base64_encoding(self, content: str):
        return re.finditer(
            r"(^|\s+)[\"']?((?:[A-Za-z0-9+\/]{4})*(?:[A-Za-z0-9+\/]{4}|[A-Za-z0-9+\/]{3}=|[A-Za-z0-9+\/]{2}={2}))[\"']",
            content,
            flags=re.RegexFlag.MULTILINE,
        )
