# auto-generated file
import _cffi_backend

ffi = _cffi_backend.FFI('_btclib_libsecp256k1',
    _version = 0x2601,
    _types = b'\x00\x00\xA5\x0D\x00\x00\xDE\x03\x00\x00\xE5\x03\x00\x00\x00\x0F\x00\x00\xA5\x0D\x00\x00\xDE\x03\x00\x00\xDF\x03\x00\x00\xDF\x03\x00\x00\x00\x0F\x00\x00\xA5\x0D\x00\x00\x05\x11\x00\x00\x06\x11\x00\x00\x02\x11\x00\x00\x00\x0F\x00\x00\xA5\x0D\x00\x00\x05\x11\x00\x00\x06\x11\x00\x00\x02\x11\x00\x00\x1C\x01\x00\x00\x00\x0F\x00\x00\xA5\x0D\x00\x00\x05\x11\x00\x00\x06\x11\x00\x00\x02\x11\x00\x00\x02\x11\x00\x00\xBA\x03\x00\x00\xEC\x03\x00\x00\x00\x0F\x00\x00\xA5\x0D\x00\x00\x05\x11\x00\x00\x07\x11\x00\x00\x02\x11\x00\x00\xE1\x03\x00\x00\x00\x0F\x00\x00\xA5\x0D\x00\x00\x05\x11\x00\x00\xE0\x03\x00\x00\x02\x11\x00\x00\x00\x0F\x00\x00\xA5\x0D\x00\x00\x05\x11\x00\x00\xE1\x03\x00\x00\x00\x0F\x00\x00\xA5\x0D\x00\x00\x05\x11\x00\x00\x29\x11\x00\x00\xE0\x03\x00\x00\x00\x0F\x00\x00\xA5\x0D\x00\x00\x05\x11\x00\x00\x29\x11\x00\x00\x20\x03\x00\x00\x1C\x01\x00\x00\x00\x0F\x00\x00\xA5\x0D\x00\x00\x05\x11\x00\x00\x29\x11\x00\x00\xE4\x03\x00\x00\x02\x11\x00\x00\x00\x0F\x00\x00\xA5\x0D\x00\x00\x05\x11\x00\x00\x29\x11\x00\x00\x02\x11\x00\x00\x00\x0F\x00\x00\xA5\x0D\x00\x00\x05\x11\x00\x00\x29\x11\x00\x00\x02\x11\x00\x00\x1C\x01\x00\x00\x00\x0F\x00\x00\xA5\x0D\x00\x00\x05\x11\x00\x00\x20\x11\x00\x00\x20\x11\x00\x00\x00\x0F\x00\x00\xA5\x0D\x00\x00\x05\x11\x00\x00\xE4\x03\x00\x00\xA5\x03\x00\x00\x2E\x11\x00\x00\x00\x0F\x00\x00\xA5\x0D\x00\x00\x05\x11\x00\x00\x4E\x11\x00\x00\x4F\x11\x00\x00\x20\x11\x00\x00\x00\x0F\x00\x00\xA5\x0D\x00\x00\x05\x11\x00\x00\x4E\x11\x00\x00\x02\x11\x00\x00\x00\x0F\x00\x00\xA5\x0D\x00\x00\x05\x11\x00\x00\x39\x11\x00\x00\x39\x11\x00\x00\x00\x0F\x00\x00\xA5\x0D\x00\x00\x05\x11\x00\x00\xE5\x03\x00\x00\x00\x0F\x00\x00\xA5\x0D\x00\x00\x05\x11\x00\x00\x64\x11\x00\x00\x07\x11\x00\x00\x00\x0F\x00\x00\xA5\x0D\x00\x00\x05\x11\x00\x00\x64\x11\x00\x00\x2E\x11\x00\x00\x00\x0F\x00\x00\xA5\x0D\x00\x00\x05\x11\x00\x00\x64\x11\x00\x00\x39\x11\x00\x00\x00\x0F\x00\x00\xA5\x0D\x00\x00\x05\x11\x00\x00\x64\x11\x00\x00\x12\x03\x00\x00\x07\x11\x00\x00\x00\x0F\x00\x00\xA5\x0D\x00\x00\x05\x11\x00\x00\x64\x11\x00\x00\x78\x11\x00\x00\x20\x11\x00\x00\x08\x01\x00\x00\x00\x0F\x00\x00\xA5\x0D\x00\x00\x05\x11\x00\x00\x64\x11\x00\x00\x02\x11\x00\x00\x00\x0F\x00\x00\xA5\x0D\x00\x00\x05\x11\x00\x00\x64\x11\x00\x00\x02\x11\x00\x00\x2E\x11\x00\x00\x02\x11\x00\x00\x00\x0F\x00\x00\xA5\x0D\x00\x00\x05\x11\x00\x00\x64\x11\x00\x00\x02\x11\x00\x00\x1C\x01\x00\x00\x2E\x11\x00\x00\xE2\x03\x00\x00\x00\x0F\x00\x00\xA5\x0D\x00\x00\x05\x11\x00\x00\x64\x11\x00\x00\x02\x11\x00\x00\x1C\x01\x00\x00\x02\x11\x00\x00\x1C\x01\x00\x00\x00\x0F\x00\x00\xA5\x0D\x00\x00\x05\x11\x00\x00\x02\x11\x00\x00\x00\x0F\x00\x00\xA5\x0D\x00\x00\x05\x11\x00\x00\x02\x11\x00\x00\x07\x01\x00\x00\x39\x11\x00\x00\x02\x11\x00\x00\x00\x0F\x00\x00\xA5\x0D\x00\x00\x05\x11\x00\x00\x02\x11\x00\x00\x02\x11\x00\x00\x1C\x01\x00\x00\x39\x11\x00\x00\x00\x0F\x00\x00\xA5\x0D\x00\x00\x64\x11\x00\x00\x02\x11\x00\x00\x1C\x01\x00\x00\x02\x11\x00\x00\x02\x11\x00\x00\x02\x11\x00\x00\x1C\x01\x00\x00\xEC\x03\x00\x00\x00\x0F\x00\x00\xA5\x0D\x00\x00\x64\x11\x00\x00\x02\x11\x00\x00\x02\x11\x00\x00\x02\x11\x00\x00\xB8\x11\x00\x00\x08\x01\x00\x00\x00\x0F\x00\x00\x01\x0D\x00\x00\x05\x11\x00\x00\x00\x0F\x00\x00\x01\x0D\x00\x00\x08\x01\x00\x00\x00\x0F\x00\x00\xDA\x0D\x00\x00\x05\x11\x00\x00\x1C\x01\x00\x00\x00\x0F\x00\x00\xEC\x0D\x00\x00\xDC\x03\x00\x00\xB8\x11\x00\x00\x00\x0F\x00\x00\xEC\x0D\x00\x00\x01\x11\x00\x00\x00\x0F\x00\x00\xEC\x0D\x00\x00\x01\x11\x00\x00\xCC\x03\x00\x00\x1A\x11\x00\x00\x00\x0F\x00\x00\xEC\x0D\x00\x00\x05\x11\x00\x00\xE3\x03\x00\x00\x00\x0F\x00\x00\x02\x01\x00\x00\xB0\x03\x00\x00\x05\x09\x00\x00\x00\x09\x00\x00\x01\x09\x00\x00\x02\x09\x00\x00\x03\x09\x00\x00\x06\x09\x00\x00\x04\x09\x00\x00\x04\x01\x00\x00\xE5\x05\x00\x00\x00\x04\x00\x00\xE5\x05\x00\x00\x00\x40\x00\x00\xE5\x05\x00\x00\x00\x60\x00\x00\x00\x01',
    _globals = (b'\x00\x00\xC2\x23secp256k1_context_clone',0,b'\x00\x00\xC5\x23secp256k1_context_create',0,b'\x00\x00\xD0\x23secp256k1_context_destroy',0,b'\x00\x00\x05\x21secp256k1_context_no_precomp',0,b'\x00\x00\x00\x23secp256k1_context_randomize',0,b'\x00\x00\xD3\x23secp256k1_context_set_error_callback',0,b'\x00\x00\xD3\x23secp256k1_context_set_illegal_callback',0,b'\x00\x00\x62\x23secp256k1_ec_privkey_negate',0,b'\x00\x00\x82\x23secp256k1_ec_privkey_tweak_add',0,b'\x00\x00\x82\x23secp256k1_ec_privkey_tweak_mul',0,b'\x00\x00\x47\x23secp256k1_ec_pubkey_cmp',0,b'\x00\x00\x30\x23secp256k1_ec_pubkey_combine',0,b'\x00\x00\x3C\x23secp256k1_ec_pubkey_create',0,b'\x00\x00\x27\x23secp256k1_ec_pubkey_negate',0,b'\x00\x00\x41\x23secp256k1_ec_pubkey_parse',0,b'\x00\x00\x7B\x23secp256k1_ec_pubkey_serialize',0,b'\x00\x00\x3C\x23secp256k1_ec_pubkey_tweak_add',0,b'\x00\x00\x3C\x23secp256k1_ec_pubkey_tweak_mul',0,b'\x00\x00\x62\x23secp256k1_ec_seckey_negate',0,b'\x00\x00\x82\x23secp256k1_ec_seckey_tweak_add',0,b'\x00\x00\x82\x23secp256k1_ec_seckey_tweak_mul',0,b'\x00\x00\x9E\x23secp256k1_ec_seckey_verify',0,b'\x00\x00\x14\x23secp256k1_ecdsa_sign',0,b'\x00\x00\x04\x23secp256k1_ecdsa_signature_normalize',0,b'\x00\x00\x09\x23secp256k1_ecdsa_signature_parse_compact',0,b'\x00\x00\x0E\x23secp256k1_ecdsa_signature_parse_der',0,b'\x00\x00\x66\x23secp256k1_ecdsa_signature_serialize_compact',0,b'\x00\x00\x75\x23secp256k1_ecdsa_signature_serialize_der',0,b'\x00\x00\x1C\x23secp256k1_ecdsa_verify',0,b'\x00\x00\x22\x23secp256k1_keypair_create',0,b'\x00\x00\x2B\x23secp256k1_keypair_pub',0,b'\x00\x00\x6B\x23secp256k1_keypair_sec',0,b'\x00\x00\x4C\x23secp256k1_keypair_xonly_pub',0,b'\x00\x00\x22\x23secp256k1_keypair_xonly_tweak_add',0,b'\x00\x00\xDD\x25secp256k1_nonce_function_bip340',0,b'\x00\x00\x19\x25secp256k1_nonce_function_default',0,b'\x00\x00\x19\x25secp256k1_nonce_function_rfc6979',0,b'\x00\x00\x87\x23secp256k1_schnorrsig_sign',0,b'\x00\x00\x87\x23secp256k1_schnorrsig_sign32',0,b'\x00\x00\x8E\x23secp256k1_schnorrsig_sign_custom',0,b'\x00\x00\xA9\x23secp256k1_schnorrsig_verify',0,b'\x00\x00\xC8\x23secp256k1_scratch_space_create',0,b'\x00\x00\xD8\x23secp256k1_scratch_space_destroy',0,b'\x00\x00\x96\x23secp256k1_tagged_sha256',0,b'\x00\x00\x5D\x23secp256k1_xonly_pubkey_cmp',0,b'\x00\x00\x52\x23secp256k1_xonly_pubkey_from_pubkey',0,b'\x00\x00\x58\x23secp256k1_xonly_pubkey_parse',0,b'\x00\x00\x70\x23secp256k1_xonly_pubkey_serialize',0,b'\x00\x00\x36\x23secp256k1_xonly_pubkey_tweak_add',0,b'\x00\x00\xA2\x23secp256k1_xonly_pubkey_tweak_add_check',0),
    _struct_unions = ((b'\x00\x00\x00\xDF\x00\x00\x00\x02$secp256k1_ecdsa_signature',b'\x00\x00\xE8\x11data'),(b'\x00\x00\x00\xE0\x00\x00\x00\x02$secp256k1_keypair',b'\x00\x00\xEA\x11data'),(b'\x00\x00\x00\xE1\x00\x00\x00\x02$secp256k1_pubkey',b'\x00\x00\xE8\x11data'),(b'\x00\x00\x00\xE2\x00\x00\x00\x02$secp256k1_schnorrsig_extraparams',b'\x00\x00\xE6\x11magic',b'\x00\x00\xDD\x11noncefp',b'\x00\x00\xB8\x11ndata'),(b'\x00\x00\x00\xE4\x00\x00\x00\x02$secp256k1_xonly_pubkey',b'\x00\x00\xE8\x11data'),(b'\x00\x00\x00\xDE\x00\x00\x00\x10secp256k1_context_struct',),(b'\x00\x00\x00\xE3\x00\x00\x00\x10secp256k1_scratch_space_struct',)),
    _typenames = (b'\x00\x00\x00\xDEsecp256k1_context',b'\x00\x00\x00\xDFsecp256k1_ecdsa_signature',b'\x00\x00\x00\xE0secp256k1_keypair',b'\x00\x00\x00\x19secp256k1_nonce_function',b'\x00\x00\x00\xDDsecp256k1_nonce_function_hardened',b'\x00\x00\x00\xE1secp256k1_pubkey',b'\x00\x00\x00\xE2secp256k1_schnorrsig_extraparams',b'\x00\x00\x00\xE3secp256k1_scratch_space',b'\x00\x00\x00\xE4secp256k1_xonly_pubkey'),
)
