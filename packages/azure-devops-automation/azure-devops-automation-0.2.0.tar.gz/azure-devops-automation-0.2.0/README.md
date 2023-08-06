# ADO Automation

[![Build Status](https://dev.azure.com/MusicalNinjas/ADO/_apis/build/status/CI-regression?branchName=working)](https://dev.azure.com/MusicalNinjas/ADO/_build/latest?definitionId=8&branchName=working)
![[Azure DevOps coverage (branch)]](https://img.shields.io/azure-devops/coverage/MusicalNinjas/ADO/8/working)
![[Licence]](https://img.shields.io/badge/licence-EUPL1.2-blue)

## Introduction

A collection of automation tools to use in ADO pipelines and webhooks

## Installation

`pip install azure-devops-automation`

## Pull Request functions

A sample `yaml` file is included which runs `changelog` and then `checkin` for the current PR if included in the PR Build validation policies

### changelog

Updates (and creates if required) a CHANGELOG markdown file using data from a given Pull Request

```bash
python -m ado_automation.PR changelog --help
usage: ado_automations.PR changelog [-h] --path PATH --collectionuri COLLECTIONURI --project PROJECT --pr PR

options:
  -h, --help            show this help message and exit
  --path PATH           relative path to changelog file, including filename
  --collectionuri COLLECTIONURI
                        base uri to ADO organisation
  --project PROJECT     ADO project name
  --pr PR               pull request ID
```

### checkin

Commits and pushes any changes made in the detached head state after a PR merge into the PR source branch. Commits with the name and email address of the PR author, pushes as BuildService.

```bash
python -m ado_automation.PR checkin --help
usage: ado_automations.PR checkin [-h] --collectionuri COLLECTIONURI --project PROJECT --pr PR [-v]

options:
  -h, --help            show this help message and exit
  --collectionuri COLLECTIONURI
                        base uri to ADO organisation
  --project PROJECT     ADO project name
  --pr PR               pull request ID
  -v, --verbosity       increase output verbosity
  ```

## Build and Test

Tests are written for pytest in `/tests/test_*.py`

## Contribute

- [Code repository (ADO)](https://dev.azure.com/MusicalNinjas/_git/ADO)
- [Homepage](https://dev.azure.com/MusicalNinjas/ADO)

## What's New?

[See CHANGELOG](./CHANGELOG.md)

## Coming Next

- Validate against complex and edge cases (eg main updated by other working branches since creating source branch)
- Create setup script to generate yaml templates
- add section markers to CHANGELOG to allow import into README
- Azure-Function to call via Webhook to update parent/children items when changing a work item on ADO Boards
