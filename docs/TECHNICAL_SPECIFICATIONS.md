---
uid: goldilocks.technical
title: Technical Specifications
description: Architecture, performance metrics, and development commands for Goldilocks
author: Goldilocks Development Team
ms.date: 2024-09-24
---

## Quick Reference

| Component    | Version     | Status | Performance Target |
| ------------ | ----------- | ------ | ------------------ |
| Python       | 3.14.0      | ✅     | <100ms startup     |
| Flask        | 3.x         | ✅     | <50ms response     |
| Docker       | Multi-stage | ✅     | <100MB runtime     |
| Tests        | 100% pass   | ✅     | <5s execution      |
| DevContainer | Optimized   | ✅     | <30s rebuild       |

## Architecture Checklist

### ✅ Completed Optimizations

- [x] Test Structure: Moved to src/goldilocks/tests/ for package inclusion
- [x] Import System: Fixed all import errors, 100% pytest pass rate
- [x] DevContainer: Removed unnecessary features, added volume caching
- [x] Docker Multi-Stage: Separate build/tools/runtime images
- [x] Python Bytecode: Precompilation scripts with optimization level 2
- [x] File Organization: Config, docs, infrastructure, scripts domains
- [x] Caching System: devcontainer-lock.json for build reproducibility

## Development Commands

Essential Commands:

- npm run test:e2e # E2E tests with Cypress
- python -m pytest # Unit tests (100% pass)
- scripts/compile-bytecode.ps1 # Bytecode compilation
- docker-compose --profile dev up # Development container
- docker-compose --profile prod up # Production container

Build Commands:

- ./infrastructure/docker/scripts/compose.sh development build # Multi-stage Docker build
- .devcontainer/scripts/generate-lock.sh # Update cache manifest
- ./infrastructure/docker/scripts/test-infrastructure.sh # Infrastructure testing

## File Locations

- config/ # Tool configurations (pytest, cypress, pre-commit)
- docs/ # Documentation (README, specifications)
- infrastructure/ # Docker multi-stage builds, K8s manifests
- scripts/ # Build automation (bytecode, caching)
- src/goldilocks/ # Source code and tests
- frontend/static/ # CSS, JS, HTML assets

## Next Actions

1. Validate Performance: Measure container sizes and startup times
2. UI Enhancement: Responsive CSS architecture
3. Error Handling: Structured exception handling throughout app
4. Production Testing: Load testing and optimization validation

## Troubleshooting

| Issue                  | Quick Fix                                            |
| ---------------------- | ---------------------------------------------------- |
| Import errors          | python -m pytest src/goldilocks/tests/               |
| Container rebuild slow | Check devcontainer-lock.json cache                   |
| Tests failing          | Verify pytest config points to src/goldilocks/tests/ |
| Large image size       | Use multi-stage runtime target                       |
| Bytecode not working   | Run scripts/compile-bytecode.ps1                     |
