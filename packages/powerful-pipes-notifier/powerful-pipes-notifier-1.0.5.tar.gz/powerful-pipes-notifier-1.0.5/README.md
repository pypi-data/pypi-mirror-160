********************************************************************************************
Powerful Pipes Notifier - Multi-Channel notification tool with the power of UNIX Pipes
********************************************************************************************

![License](https://img.shields.io/badge/License-Apache2-SUCCESS)
![Pypi](https://img.shields.io/pypi/v/powerful-pipes-notifier)
![Python Versions](https://img.shields.io/badge/Python-3.8%20%7C%203.9%20%7C%203.10-blue)

![Logo](https://raw.githubusercontent.com/42Crunch/powerful-pipes-notifier/main/docs/logo-250x250.png)

In a nutshell ``Powerful Pipes Notifier`` is a notification tool to forward STDIN data to different destinations.

# Install

```bash
> pip install powerful-pipes-notifier 
```

# Quick Start

Powerful pipes notifier send to a destination the stdin data, line by line.

Examples:

**HTTP Web Hook**

```bash
> notifier -d http://localhost/webhook
```

**Web Socket Hook**

```bash
> notifier ws://localhost/websocket-hook
```

# Allowed destinations

Currently, these are the implemented schemas:

- http://URI -> webhook
- ws://URI -> websocket
- mongodb://user:password@host:port/?db=DATABASE&collection=COLLECTION 

### MongoDB examples

```bash
> docker-compose -f docker-compose.mongo.yaml up -d
> cat examples/localhost_meta.txt | notifier -d "mongodb://root:example@127.0.0.1:27900/?db=notifier&collection=logs" 
```

> NOTE: Pay attention of symbol "?" in the URI after the port slash.

# Rules engine

You can set a rule that tell to notifier if notify or not.

Rules are based in JSONPath standard and will try to match it in the input JSON data.

Usage example:

```bash
> notifier -d http://localhost/webhook -R "_meta.dataSource.sourceName == 'har asdf'"
> notifier -d http://localhost/webhook -R "_meta.summary.current == _meta.summary.total"
```

# Documentation

You can find the complete documentation at: [Documentation](https://powerful-pipes-notifier.pythonhosted.org).

# Authors

Powerful Pipes Notifier was made by 42Crunch Research Team:

- [jc42](https://github.com/jc42c)
- [cr0hn](https://github.com/cr0hn)


# License

Powerful Pipes Notifier is Open Source and available under the [AGPLv3+](https://github.com/42Crunch/powerful-pipes-notifier/blob/main/LICENSE).

# Contributions

Contributions are very welcome. See [CONTRIBUTING.md](https://github.com/42Crunch/powerful-pipes-notifier/blob/main/CONTRIBUTING.md>) or skim existing tickets to see where you could help out.

# Acknowledgements

Project logo thanks to [Pipe icons created by starline - Flaticon ](https://www.freepik.com/vectors/blue-arrow).

