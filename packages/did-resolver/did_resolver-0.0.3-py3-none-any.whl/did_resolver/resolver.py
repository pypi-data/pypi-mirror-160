#!/usr/bin/env python3

import abc
import re
from typing import Dict, List, Literal, Mapping, Protocol, Type, TypedDict, Union

from typing_extensions import NotRequired

Params = Dict[str, str]


class ParsedDID(TypedDict):
    id: str
    did: str
    did_url: str
    method: str
    path: NotRequired[str]
    fragment: NotRequired[str]
    query: NotRequired[str]
    params: NotRequired[Params]


class DidResolutionOptions(TypedDict):
    accept: NotRequired[str]


class DIDResolutionMetadata(TypedDict):
    contentType: NotRequired[str]
    error: NotRequired[
        Union[
            Literal[
                "invalidDid",
                "notFound",
                "representationNotSupported",
                "unsupportedDidMethod",
            ],
            str,
        ]
    ]


class ServiceEndpoint(TypedDict):
    id: str
    type: str
    serviceEndpoint: str
    description: NotRequired[str]


class JsonWebKey(TypedDict):
    kty: str
    alg: NotRequired[str]
    crv: NotRequired[str]
    e: NotRequired[str]
    ext: NotRequired[bool]
    key_ops: NotRequired[List[str]]
    kid: NotRequired[str]
    n: NotRequired[str]
    use: NotRequired[str]
    x: NotRequired[str]
    y: NotRequired[str]


class VerificationMethod(TypedDict):
    id: str
    type: str
    controller: str
    publicKeyJwk: NotRequired[JsonWebKey]
    publicKeyBase58: NotRequired[str]
    publicKeyBase64: NotRequired[str]
    publicKeyHex: NotRequired[str]
    publicKeyMultibase: NotRequired[str]
    publicKeyAccountId: NotRequired[str]
    ethereumAddress: NotRequired[str]
    blockchainAccountId: NotRequired[str]


class DIDDocument(TypedDict):
    id: str
    context: Union[str, List[str]]
    alsoKnownAs: NotRequired[List[str]]
    controller: NotRequired[Union[str, List[str]]]
    service: NotRequired[List[ServiceEndpoint]]
    publicKey: NotRequired[List[VerificationMethod]]
    # KeyCapabilitySection
    authentication: NotRequired[Union[str, VerificationMethod]]
    assertionMethod: NotRequired[Union[str, VerificationMethod]]
    keyAgreement: NotRequired[Union[str, VerificationMethod]]
    capabilityInvocation: NotRequired[Union[str, VerificationMethod]]
    capabilityDelegation: NotRequired[Union[str, VerificationMethod]]


class DIDDocumentMetadata(TypedDict):
    created: NotRequired[str]
    updated: NotRequired[str]
    deactivated: NotRequired[bool]
    versionId: NotRequired[str]
    nextUpdate: NotRequired[str]
    nextVersionId: NotRequired[str]
    equivalentId: NotRequired[str]
    canonicalId: NotRequired[str]


class DIDResolutionResult(TypedDict):
    didResolutionMetadata: DIDResolutionMetadata
    didDocument: Union[DIDDocument, None]
    didDocumentMetadata: DIDDocumentMetadata


class Resolvable:
    @abc.abstractmethod
    def resolve(self, did_url: str) -> DIDResolutionResult:
        pass


# DIDResolver = Callable[[str, ParsedDID, Resolvable], DIDResolutionResult]
# https://stackoverflow.com/questions/57837609/python-typing-signature-typing-callable-for-function-with-kwargs
class DIDResolver(Protocol):
    def __call__(
        self, did: str, parsed: ParsedDID, resolver: Resolvable
    ) -> DIDResolutionResult:
        pass


ResolverRegistry = Mapping[str, DIDResolver]

EMPTY_RESULT: DIDResolutionResult = {
    "didResolutionMetadata": {},
    "didDocument": None,
    "didDocumentMetadata": {},
}

PCT_ENCODED = "(?:%[0-9a-fA-F]{2})"
ID_CHAR = f"(?:[a-zA-Z0-9._-]|{PCT_ENCODED})"
METHOD = "([a-z0-9]+)"
METHOD_ID = f"((?:{ID_CHAR}*:)*({ID_CHAR}+))"
PARAM_CHAR = "[a-zA-Z0-9_.:%-]"
PARAM = f";{PARAM_CHAR}+={PARAM_CHAR}*"
PARAMS = f"(({PARAM})*)"
PATH = "(/[^#?]*)?"
QUERY = "([?][^#]*)?"
FRAGMENT = "(#.*)?"
DID_MATCHER = f"^did:{METHOD}:{METHOD_ID}{PARAMS}{PATH}{QUERY}{FRAGMENT}$"


def parse(did_url: str) -> Union[ParsedDID, None]:
    if did_url == "":
        return None
    match = re.search(DID_MATCHER, did_url)
    if match is not None:
        groups = match.groups()
        if groups is not None:
            parts: ParsedDID = {
                "did": f"did:{groups[0]}:{groups[1]}",
                "method": groups[0],
                "id": groups[1],
                "did_url": did_url,
            }

            if (
                groups[3] is not None
                and groups[3] != ""
                and isinstance(groups[3][1:], str)
            ):
                params = groups[3][1:]
                s1 = params.split(";")
                parts["params"] = {}
                for param in s1:
                    s2 = param.split("=")
                    [key, val] = s2
                    parts["params"][key] = val

            if groups[5] is not None:
                parts["path"] = groups[5]
            if groups[6] is not None:
                parts["query"] = groups[6][1:]
            if groups[7] is not None:
                parts["fragment"] = groups[7][1:]
            return parts
    return None


class Resolver(Resolvable):
    def __init__(self, registry: ResolverRegistry = {}):
        self.__registry = registry

    def resolve(self, did_url: str) -> DIDResolutionResult:
        parsed = parse(did_url)
        if parsed is None:
            return DIDResolutionResult(
                didResolutionMetadata={"error": "invalidDid"},
                didDocument=EMPTY_RESULT["didDocument"],
                didDocumentMetadata=EMPTY_RESULT["didDocumentMetadata"],
            )
        resolver_name = parsed["method"]
        res = self.__registry.get(resolver_name, None)
        if res is None:
            return DIDResolutionResult(
                didResolutionMetadata={"error": "unsupportedDidMethod"},
                didDocument=EMPTY_RESULT["didDocument"],
                didDocumentMetadata=EMPTY_RESULT["didDocumentMetadata"],
            )
        resolver = self.__registry[resolver_name]
        return resolver(did_url, parsed, self)
