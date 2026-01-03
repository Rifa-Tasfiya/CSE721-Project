import numpy as np

alphabet = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
]


def clean_text(text):
    text = text.lower()
    cleaned = ""
    for ch in text:
        if ch in alphabet:
            cleaned += ch
    return cleaned


def euclid_gcd(a, b):
    if b == 0:
        return a
    else:
        return euclid_gcd(b, a % b)


def mod_inverse(a, m):
    a = a % m
    for i in range(m):
        if (a * i) % m == 1:
            return i
    return None


def det_2x2_mod26(M):
    return (int(M[0, 0]) * int(M[1, 1]) - int(M[0, 1]) * int(M[1, 0])) % 26


def inv_2x2_mod26(M):
    det = det_2x2_mod26(M)
    det_inv = mod_inverse(det, 26)
    if det_inv is None:
        return None

    a = int(M[0, 0])
    b = int(M[0, 1])
    c = int(M[1, 0])
    d = int(M[1, 1])

    adj = np.array([[d, -b],
                    [-c, a]], dtype=int)

    result = (det_inv * adj) % 26
    return result


def text_to_nums(text):
    nums = []
    for ch in text:
        nums.append(alphabet.index(ch))
    return nums


def parse_comma_list(s):
    parts = s.split(",")
    items = []
    for p in parts:
        item = p.strip()
        if item != "":
            items.append(item)
    return items


def recover_hill2x2_key_from_strings(plaintexts_csv, ciphertexts_csv):
    plaintext_list = parse_comma_list(plaintexts_csv)
    ciphertext_list = parse_comma_list(ciphertexts_csv)

    if len(plaintext_list) == 0 or len(ciphertext_list) == 0:
        return None, "Both plaintext and ciphertext lists must be non-empty."

    if len(plaintext_list) != len(ciphertext_list):
        return None, "Number of plaintexts and ciphertexts must be the same."

    # Collect digraphs for each pair separately
    all_digraph_pairs_list = []  # List of lists of (P_digraph, C_digraph) tuples for each pair

    for idx in range(len(plaintext_list)):
        pt = clean_text(plaintext_list[idx])
        ct = clean_text(ciphertext_list[idx])

        if len(pt) == 0 or len(ct) == 0:
            return None, f"Pair {idx + 1}: plaintext/ciphertext becomes empty after cleaning."

        if len(pt) != len(ct):
            return None, f"Pair {idx + 1}: plaintext and ciphertext must have same length after cleaning."

        if len(pt) % 2 != 0:
            pt = pt[:-1]
            ct = ct[:-1]

        if len(pt) < 2:
            return None, f"Pair {idx + 1}: not enough text (need at least 2 chars)."

        p_nums = text_to_nums(pt)
        c_nums = text_to_nums(ct)

        # Collect digraphs for this pair
        digraph_pairs = []
        for i in range(0, len(p_nums), 2):
            if i + 1 < len(p_nums):
                P_digraph = [p_nums[i], p_nums[i + 1]]
                C_digraph = [c_nums[i], c_nums[i + 1]]
                digraph_pairs.append((P_digraph, C_digraph))

        all_digraph_pairs_list.append(digraph_pairs)

    # Check if there are enough digraph pairs
    if any(len(pairs) < 2 for pairs in all_digraph_pairs_list):
        return None, "Need at least 2 digraph pairs for each plaintext-ciphertext pair."

    # Try to recover the key using digraphs from each pair
    for digraph_pairs in all_digraph_pairs_list:
        P_digraphs = [pair[0] for pair in digraph_pairs]
        C_digraphs = [pair[1] for pair in digraph_pairs]
        total = len(P_digraphs)

        # PASS 1: ROW model (C = P×K)
        for i in range(total):
            for j in range(i + 1, total):
                P_mat = np.array([P_digraphs[i], P_digraphs[j]], dtype=int)
                C_mat = np.array([C_digraphs[i], C_digraphs[j]], dtype=int)

                detP = det_2x2_mod26(P_mat)
                if euclid_gcd(detP, 26) != 1:
                    continue

                P_inv = inv_2x2_mod26(P_mat)
                if P_inv is None:
                    continue

                K_candidate = np.dot(P_inv, C_mat) % 26

                # Verify on ALL digraph pairs from ALL pairs
                verified = True
                for pairs in all_digraph_pairs_list:
                    for P_digraph, C_digraph in pairs:
                        P_vec = np.array(P_digraph, dtype=int).reshape(1, 2)
                        C_vec = np.array(C_digraph, dtype=int).reshape(1, 2)
                        computed = np.dot(P_vec, K_candidate) % 26
                        if not np.array_equal(computed, C_vec):
                            verified = False
                            break
                    if not verified:
                        break

                if verified:
                    return K_candidate, "Recovered key."

        # PASS 2: COLUMN model (C = K×P)
        for i in range(total):
            for j in range(i + 1, total):
                P_mat = np.array([[P_digraphs[i][0], P_digraphs[j][0]],
                                  [P_digraphs[i][1], P_digraphs[j][1]]], dtype=int)

                C_mat = np.array([[C_digraphs[i][0], C_digraphs[j][0]],
                                  [C_digraphs[i][1], C_digraphs[j][1]]], dtype=int)

                detP = det_2x2_mod26(P_mat)
                if euclid_gcd(detP, 26) != 1:
                    continue

                P_inv = inv_2x2_mod26(P_mat)
                if P_inv is None:
                    continue

                K_candidate = np.dot(C_mat, P_inv) % 26

                # Verify on ALL digraph pairs from ALL pairs
                verified = True
                for pairs in all_digraph_pairs_list:
                    for P_digraph, C_digraph in pairs:
                        P_col = np.array([[P_digraph[0]], [P_digraph[1]]], dtype=int)
                        C_col = np.array([[C_digraph[0]], [C_digraph[1]]], dtype=int)
                        computed = np.dot(K_candidate, P_col) % 26
                        if not np.array_equal(computed, C_col):
                            verified = False
                            break
                    if not verified:
                        break

                if verified:
                    return K_candidate, "Recovered key."

    return None, "Could not recover a key from the given pairs."