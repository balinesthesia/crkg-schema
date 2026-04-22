# Branch protection

`main` is protected with the following rules (configured in GitHub UI):

- **Require a pull request before merging**
- **Require status checks to pass before merging**
  - `lint`
  - `schema-valid`
  - `emission-parity`
  - `fixtures-valid`
  - `build`
- **Require signed commits**
- **Require linear history** (no merge commits)
- **Include administrators** (rules apply to admins too)
