# SCA3S CLI

Toolkit to enable job submission to [SCA3S](https://sca3s.scarv.org) from the command line.

## Installation 

```bash
pip install sca3s_cli
```

## Configuration

- SCA3S CLI links to a pre-existing SCA3S account via an API token which can be obtained via the user profile page.
- Once a token is obtained and `sca3s-cli` installed, edit the config file in `~/.sca3s/config` as follows:

```bash
[default]
token
```

This will link the cli to your SCA3S account. If you possess multiple SCA3S accounts you can add additional tokens
with friendly names to the config file and utilise these tokens via the `scope` parameter in the cli.