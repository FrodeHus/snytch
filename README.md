# Ludvig security scanner

[![Ludvig scan](https://github.com/FrodeHus/ludvig/actions/workflows/main.yml/badge.svg)](https://github.com/FrodeHus/ludvig/actions/workflows/main.yml)

> Want to use Ludvig with your CI pipeline? Mosey on over to the [Ludvig Action](https://github.com/marketplace/actions/ludvig-security-scanner) :)  
> Or contribute to Ludvig's [YARA rules](https://github.com/frodehus/ludvig-rules)?

Named after Kjell Aukrust's character Ludvig who thinks everything is dangerous and is scared of the dark during the day.

_Why yet another scanner?_

Mostly because I thought it was a fun way to use YARA rules for something in addition to malware hunting and to learn how these kind of tools are made.

## Installation

Either clone this repository or install using `python -m pip install ludvig`

## Usage

The general usage of the tool can be found by running `python -m ludvig --help`

### Adding your own rules

Ludvig happily accepts YARA rules from anywhere you choose - the only requirement is that they are packaged up neatly in a `.tar.gz` format.
You can add your custom rule package using `ludvig rules add repo --name my_rules --category my_worries --url http://localhost/my_rules.tar.gz`

### Container scan

Scan container: `python -m ludvig image scan --repository <repository>`

```text
ludvig image scan --help

Command
    ludvig image scan : Scans a container image.

Arguments
    --repository [Required] : Container image to scan (ex: myimage:1.1).
    --deobfuscated          : Returns any secrets found in plaintext. Default: False.
    --include-first-layer   : Scan first layer (base image) as well - may affect speed. Default:
                              False.
    --max-file-size         : Max file size for scanning (in bytes).  Default: 10000.
    --output-sarif          : Generates SARIF report if filename is specified.
    --severity-level        : Set severity level for reporting.  Allowed values: CRITICAL, HIGH,
                              LOW, MEDIUM, UNKNOWN.  Default: MEDIUM.
```

### Filesystem scan

Scan the filesystem: `python -m ludvig fs scan --path <path>`

```text
ludvig fs scan --help

Command
    ludvig fs scan : Scans a filesystem path.

Arguments
    --path  [Required] : Path to scan.
    --deobfuscated     : Returns any secrets found in plaintext. Default: False.
    --max-file-size    : Max file size for scanning (in bytes).  Default: 10000.
    --output-sarif     : Generates SARIF report if filename is specified.
    --severity-level   : Set severity level for reporting.  Allowed values: CRITICAL, HIGH, LOW,
                         MEDIUM, UNKNOWN.  Default: MEDIUM.
```

### Adding files/directories to ignore list

Create a `.ludvignore` file such as:

```text
*.yar
debug/
```
