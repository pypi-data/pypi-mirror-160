# Equinix Resource Provider

The Equinix Resource Provider lets you manage [Equinix](http://equinix.com) resources.

## Installing

This package is available for several languages/platforms:

### Node.js (JavaScript/TypeScript)

To use from JavaScript or TypeScript in Node.js, install using either `npm`:

```bash
npm install @pulumi/equinix
```

or `yarn`:

```bash
yarn add @pulumi/equinix
```

### Python

To use from Python, install using `pip`:

```bash
pip install pulumi_equinix
```

### Go

To use from Go, use `go get` to grab the latest version of the library:

```bash
go get github.com/pulumi/pulumi-equinix/sdk/go/...
```

### .NET

To use from .NET, install using `dotnet add package`:

```bash
dotnet add package Pulumi.Equinix
```

## Configuration

The following configuration points are available for the `equinix` provider:

- `equinix:authToken` (environment: `METAL_AUTH_TOKEN`) - This is your Equinix Metal API Auth token.
- `equinix:clientId` (environment: `EQUINIX_API_CLIENTID`) - API Consumer Key available under "My Apps" in developer portal.
- `equinix:clientSecret` (environment: `EQUINIX_API_CLIENTSECRET`) - API Consumer secret available under "My Apps" in developer portal.
- `equinix:token` (environment: `EQUINIX_API_TOKEN`) - API tokens are generated from API Consumer clients using the OAuth2 API.
- `equinix:endpoint` (environment: `EQUINIX_API_ENDPOINT`) - The Equinix API base URL to point out desired environment.

## Reference

For detailed reference documentation, please visit [the Pulumi registry](https://www.pulumi.com/registry/packages/equinix/api-docs/).
