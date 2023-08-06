#!/usr/bin/env python3

import pytest

from did_resolver import Resolver, parse


class TestParse:
    def test_base(self):
        did = "did:uport:2nQtiQG6Cgm1GYTBaaKAgr76uY7iSexUkqX"
        p = parse(did)
        assert p == {
            "method": "uport",
            "id": "2nQtiQG6Cgm1GYTBaaKAgr76uY7iSexUkqX",
            "did": "did:uport:2nQtiQG6Cgm1GYTBaaKAgr76uY7iSexUkqX",
            "did_url": "did:uport:2nQtiQG6Cgm1GYTBaaKAgr76uY7iSexUkqX",
        }

    def test_path(self):
        did = "did:uport:2nQtiQG6Cgm1GYTBaaKAgr76uY7iSexUkqX/some/path"
        p = parse(did)
        assert p == {
            "method": "uport",
            "id": "2nQtiQG6Cgm1GYTBaaKAgr76uY7iSexUkqX",
            "did": "did:uport:2nQtiQG6Cgm1GYTBaaKAgr76uY7iSexUkqX",
            "did_url": "did:uport:2nQtiQG6Cgm1GYTBaaKAgr76uY7iSexUkqX/some/path",
            "path": "/some/path",
        }

    def test_fragment(self):
        did = "did:uport:2nQtiQG6Cgm1GYTBaaKAgr76uY7iSexUkqX#fragment=123"
        p = parse(did)
        assert p == {
            "method": "uport",
            "id": "2nQtiQG6Cgm1GYTBaaKAgr76uY7iSexUkqX",
            "did": "did:uport:2nQtiQG6Cgm1GYTBaaKAgr76uY7iSexUkqX",
            "did_url": "did:uport:2nQtiQG6Cgm1GYTBaaKAgr76uY7iSexUkqX#fragment=123",
            "fragment": "fragment=123",
        }

    def test_path_and_fragment(self):
        did = "did:uport:2nQtiQG6Cgm1GYTBaaKAgr76uY7iSexUkqX/some/path#fragment=123"
        p = parse(did)
        assert p == {
            "method": "uport",
            "id": "2nQtiQG6Cgm1GYTBaaKAgr76uY7iSexUkqX",
            "did": "did:uport:2nQtiQG6Cgm1GYTBaaKAgr76uY7iSexUkqX",
            "did_url": "did:uport:2nQtiQG6Cgm1GYTBaaKAgr76uY7iSexUkqX/some/path#fragment=123",
            "path": "/some/path",
            "fragment": "fragment=123",
        }

    def test_params(self):
        did = "did:example:21tDAKCERh95uGgKbJNHYp;service=agent;foo:bar=high"
        p = parse(did)
        assert p == {
            "did": "did:example:21tDAKCERh95uGgKbJNHYp",
            "method": "example",
            "id": "21tDAKCERh95uGgKbJNHYp",
            "did_url": "did:example:21tDAKCERh95uGgKbJNHYp;service=agent;foo:bar=high",
            "params": {"service": "agent", "foo:bar": "high"},
        }

    def test_query_and_params(self):
        did = "did:example:21tDAKCERh95uGgKbJNHYp;service=agent;foo:bar=high?foo=bar"
        p = parse(did)
        assert p == {
            "method": "example",
            "id": "21tDAKCERh95uGgKbJNHYp",
            "did_url": "did:example:21tDAKCERh95uGgKbJNHYp;service=agent;foo:bar=high?foo=bar",
            "did": "did:example:21tDAKCERh95uGgKbJNHYp",
            "query": "foo=bar",
            "params": {
                "service": "agent",
                "foo:bar": "high",
            },
        }

    def test_query_and_path_and_fragment_and_params(self):
        did = "did:example:21tDAKCERh95uGgKbJNHYp;service=agent;foo:bar=high/some/path?foo=bar#key1"
        p = parse(did)
        assert p == {
            "method": "example",
            "id": "21tDAKCERh95uGgKbJNHYp",
            "did_url": "did:example:21tDAKCERh95uGgKbJNHYp;service=agent;foo:bar=high/some/path?foo=bar#key1",
            "did": "did:example:21tDAKCERh95uGgKbJNHYp",
            "query": "foo=bar",
            "path": "/some/path",
            "fragment": "key1",
            "params": {
                "service": "agent",
                "foo:bar": "high",
            },
        }

    def test_returns_none(self):
        assert parse("") is None
        assert parse("did:") is None
        assert parse("did:uport") is None
        assert parse("did:uport:") is None
        assert parse("did:uport:1234_12313***") is None
        assert parse("2nQtiQG6Cgm1GYTBaaKAgr76uY7iSexUkqX") is None
        assert parse("did:method:%12%1") is None
        assert parse("did:method:%1233%Ay") is None
        assert parse("did:CAP:id") is None
        assert parse("did:method:id::anotherid%r9") is None


@pytest.fixture(scope="class")
def mock_resolver():
    registry = {
        "example": lambda did, _1, _2: {
            "didResolutionMetadata": {"contentType": "application/did+ld+json"},
            "didDocument": {
                "@context": "https://w3id.org/did/v1",
                "id": did,
                "verificationMethod": [
                    {
                        "id": "owner",
                        "controller": "1234",
                        "type": "xyz",
                    },
                ],
            },
            "didDocumentMetadata": {},
        }
    }

    yield Resolver(registry)


@pytest.mark.usefixtures("mock_resolver")
class TestResolver:
    def test_fails_unhandled_methods(self, mock_resolver):
        did = "did:borg:2nQtiQG6Cgm1GY"
        assert mock_resolver.resolve(did) == {
            "didResolutionMetadata": {"error": "unsupportedDidMethod"},
            "didDocument": None,
            "didDocumentMetadata": {},
        }

    def test_fails_parse_error(self, mock_resolver):
        did = "did:borg:"
        assert mock_resolver.resolve(did) == {
            "didResolutionMetadata": {"error": "invalidDid"},
            "didDocument": None,
            "didDocumentMetadata": {},
        }

    def test_resolves_did_document(self, mock_resolver):
        did = "did:example:123456789"
        assert mock_resolver.resolve(did) == {
            "didResolutionMetadata": {"contentType": "application/did+ld+json"},
            "didDocument": {
                "@context": "https://w3id.org/did/v1",
                "id": "did:example:123456789",
                "verificationMethod": [
                    {
                        "id": "owner",
                        "controller": "1234",
                        "type": "xyz",
                    },
                ],
            },
            "didDocumentMetadata": {},
        }
