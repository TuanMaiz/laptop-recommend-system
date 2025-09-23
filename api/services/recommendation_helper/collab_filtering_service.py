import rdflib
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, XSD
import numpy as np
from collections import defaultdict
import os

BASE = "http://example.org/laptop#"
ns = Namespace(BASE)


class RDFUSM:
    def __init__(self, owl_file_path: str = None):
        if owl_file_path is None:
            # Get the directory where this script is located
            current_dir = os.path.dirname(os.path.abspath(__file__))
            owl_file_path = os.path.join(current_dir, "laptop.owl")
        self.g = rdflib.Graph()
        self.g.parse(owl_file_path, format="turtle")

    def save(self):
        self.g.serialize(destination="./laptop_res.owl", format="turtle")

    # --- Init profile from InitialAnswer (fingerprint, functionality, specs, price) ---
    def init_profile(
        self, fingerprint: str, functionality: str, specs: str, price: str
    ):
        u = ns["User_" + fingerprint]
        self.g.add((u, RDF.type, ns.User))
        # functionality
        f = ns[functionality]
        self.g.add((f, RDF.type, ns.Functionality))
        self.g.add((u, ns.HAS_FUNCREQ, f))
        # price
        p = ns[price]
        self.g.add((p, RDF.type, ns.PriceRange))
        self.g.add((u, ns.PREFERS_RANGE, p))
        # specs could be comma-separated string or single
        for sname in specs:
            sname = sname.strip()
            if not sname:
                continue
            s = ns[sname]
            self.g.add((s, RDF.type, ns.Specification))
            # optionally link functionality to spec if not present
            self.g.add((f, ns.REQUIRES, s))
        self.save()
        return True

    # --- Add/update rating triple (fingerprint, product_id, score) ---
    def rate_product(self, fingerprint: str, product_id: str, score: float):
        u = ns["User_" + fingerprint]
        p = ns[product_id]
        # ensure user/product nodes exist (product probably exists in ontology)
        self.g.add((u, RDF.type, ns.User))
        # Remove existing rating if present
        for s in list(self.g.triples((u, ns.RATED, None))):
            # s = (u, ns.RATED, obj)
            # But the score is stored as a reified or as property on blank node?
            pass
        # We'll store rating as reified via a blank node, but simpler: create a custom predicate link with score as literal attached to the edge via a node
        # Simpler approach: create a Rating node
        rid = URIRef(f"{BASE}Rating_{fingerprint}_{product_id}")
        self.g.set((rid, RDF.type, ns.Rating))
        self.g.set((rid, ns.forUser, u))
        self.g.set((rid, ns.forProduct, p))
        self.g.set((rid, ns.score, Literal(float(score), datatype=XSD.float)))
        # Also add a direct typed relationship for simpler SPARQL: u ns.RATED p .
        self.g.set((u, ns.RATED, p))
        self.save()
        return True

    # --- Get candidate laptops by ontology filtering ---
    def get_candidates_by_ontology(self, fingerprint: str):
        u = ns["User_" + fingerprint]
        candidates = set()

        # 1. Get user's functionality requirements
        for _, _, func in self.g.triples((u, ns.HAS_FUNCREQ, None)):
            # print(f"User requires functionality: {func.split('#')[-1]}")

            # 2. Find products that satisfy that functionality
            for prod, _, _ in self.g.triples((None, ns.satisfiesRequirement, func)):
                candidates.add(prod)

        # 3. Optional: filter by user preferred price range
        for _, _, pr in self.g.triples((u, ns.PREFERS_RANGE, None)):
            # print(f"User prefers price range: {pr.split('#')[-1]}")
            prcands = set()
            for prod in candidates:
                if (prod, ns.hasPriceRange, pr) in self.g:
                    prcands.add(prod)
            if prcands:
                candidates = prcands

        # 4. Return list of product URIs
        return list(candidates)

    # --- Read all ratings into user-item matrix structures ---
    def build_rating_matrix(self):
        # produce mapping: user_idx, item_idx, matrix
        users = {}
        items = {}
        ratings = []  # list of (u_idx, i_idx, score)
        # Ratings stored in Rating nodes (forUser, forProduct, score)
        for rid, _, _ in self.g.triples((None, RDF.type, ns.Rating)):
            user_nodes = list(self.g.objects(rid, ns.forUser))
            prod_nodes = list(self.g.objects(rid, ns.forProduct))
            scores = list(self.g.objects(rid, ns.score))
            if not user_nodes or not prod_nodes or not scores:
                continue
            u = user_nodes[0]
            p = prod_nodes[0]
            s = float(scores[0].toPython())
            u_str = str(u)
            p_str = str(p)
            if u_str not in users:
                users[u_str] = len(users)
            if p_str not in items:
                items[p_str] = len(items)
            ratings.append((users[u_str], items[p_str], s))
        # build matrix
        if not users or not items:
            return users, items, np.zeros((len(users), len(items)))
        mat = np.zeros((len(users), len(items)))
        for uidx, iidx, s in ratings:
            mat[uidx, iidx] = s
        return users, items, mat

    # --- compute item-based similarity (adjusted cosine) ---
    def compute_item_similarity(self, users_map, items_map, mat):
        # mat: users x items
        if mat.size == 0:
            return np.zeros((0, 0))

        # subtract user means (rows)
        user_means = np.zeros(mat.shape[0])
        for i in range(mat.shape[0]):
            rated_mask = mat[i, :] != 0
            if np.any(rated_mask):
                user_means[i] = np.mean(mat[i, rated_mask])
            else:
                user_means[i] = 0

        mat_centered = np.zeros_like(mat)
        for i in range(mat.shape[0]):
            mask = mat[i, :] != 0
            mat_centered[i, mask] = mat[i, mask] - user_means[i]

        # compute item vectors (items in columns)
        item_vectors = mat_centered.T  # items x users
        n_items = item_vectors.shape[0]

        # compute similarity matrix
        sim = np.zeros((n_items, n_items))
        norms = np.linalg.norm(item_vectors, axis=1)

        for i in range(n_items):
            for j in range(i + 1, n_items):
                if norms[i] > 0 and norms[j] > 0:
                    s = float(
                        np.dot(item_vectors[i], item_vectors[j]) / (norms[i] * norms[j])
                    )
                    sim[i, j] = s
                    sim[j, i] = s
                # diagonal is 1.0 for self-similarity
                sim[i, i] = 1.0 if norms[i] > 0 else 0.0

        return sim

    def compute_ontology_similarity(self, prod1, prod2):
        """Compute ontology-based similarity between two products"""
        score = 0.0

        # Shared functionality (via :satisfiesRequirement)
        funcs1 = set(self.g.objects(prod1, ns.satisfiesRequirement))
        funcs2 = set(self.g.objects(prod2, ns.satisfiesRequirement))
        if funcs1 & funcs2:
            score += 0.3

        # Shared price range (via :hasPriceRange)
        prices1 = set(self.g.objects(prod1, ns.hasPriceRange))
        prices2 = set(self.g.objects(prod2, ns.hasPriceRange))
        if prices1 & prices2:
            score += 0.1

        # Shared specifications (via :hasSpecification)
        specs1 = set(self.g.objects(prod1, ns.hasSpecification))
        specs2 = set(self.g.objects(prod2, ns.hasSpecification))
        overlap = len(specs1 & specs2)
        if overlap > 0:
            score += min(0.2 * overlap, 0.4)  # cap at 0.4

        return min(score, 1.0)  # normalize

    # --- predict scores for a target user for a set of candidate products ---
    def predict_scores_for_user(self, fingerprint: str, candidates, alpha=0.7):
        users_map, items_map, mat = self.build_rating_matrix()
        if not users_map or not items_map:
            return {}

        sim_cf = self.compute_item_similarity(users_map, items_map, mat)

        u_uri = str(ns["User_" + fingerprint])
        if u_uri not in users_map:
            return {}

        u_idx = users_map[u_uri]
        predictions = {}
        user_ratings = mat[u_idx, :]
        user_mean = (
            np.mean(user_ratings[user_ratings > 0]) if np.any(user_ratings > 0) else 3.0
        )

        # Create reverse mapping from index to URI for easier lookup
        idx_to_item_uri = {v: k for k, v in items_map.items()}

        for prod in candidates:
            prod_uri = str(prod)

            # Case 1: explicit rating exists
            if prod_uri in items_map:
                i_idx = items_map[prod_uri]
                if user_ratings[i_idx] != 0:
                    predictions[prod_uri] = float(user_ratings[i_idx])
                    continue

            # Case 2: CF + ontology prediction for unrated items
            rated_indices = np.where(user_ratings != 0)[0]

            if len(rated_indices) > 0:
                numer, denom = 0.0, 0.0

                # Get target item index (if exists in rating matrix)
                target_idx = items_map.get(prod_uri, None)

                for j in rated_indices:
                    cf_val = 0.0

                    # Use CF similarity if target item exists in rating matrix
                    if (
                        target_idx is not None
                        and target_idx < sim_cf.shape[0]
                        and j < sim_cf.shape[1]
                    ):
                        cf_val = sim_cf[target_idx, j]

                    # Compute ontology similarity
                    rated_prod_uri = idx_to_item_uri[j]
                    ont_val = self.compute_ontology_similarity(
                        prod, URIRef(rated_prod_uri)
                    )

                    # Combine similarities
                    sim_final = alpha * cf_val + (1 - alpha) * ont_val

                    if sim_final > 0:
                        numer += sim_final * user_ratings[j]
                        denom += sim_final

                if denom > 0:
                    pred_score = numer / denom
                    predictions[prod_uri] = float(max(0.0, min(5.0, pred_score)))
                    continue

            # Case 3: ontology-only fallback
            if len(rated_indices) > 0:
                ont_weighted_scores = []
                total_ont_sim = 0.0

                for j in rated_indices:
                    rated_prod_uri = idx_to_item_uri[j]
                    ont_val = self.compute_ontology_similarity(
                        prod, URIRef(rated_prod_uri)
                    )
                    if ont_val > 0:
                        ont_weighted_scores.append(ont_val * user_ratings[j])
                        total_ont_sim += ont_val

                if ont_weighted_scores and total_ont_sim > 0:
                    pred_score = sum(ont_weighted_scores) / total_ont_sim
                    predictions[prod_uri] = float(max(0.0, min(5.0, pred_score)))
                    continue

            # Case 4: global mean fallback
            predictions[prod_uri] = float(user_mean)

        return predictions

    # --- main recommend flow ---
    def recommend(self, fingerprint: str, top_k=5):
        candidates = self.get_candidates_by_ontology(fingerprint)
        # predict CF scores
        preds = self.predict_scores_for_user(fingerprint, candidates)

        # prepare list with ontology rank + CF score
        results = []
        for prod in candidates:
            model_vals = list(self.g.objects(prod, ns.model))
            model = str(model_vals[0]) if model_vals else prod.split("#")[-1]
            prod_uri = str(prod)
            cf_score = preds.get(prod_uri, None)
            results.append(
                {"product_uri": prod_uri, "model": model, "cf_score": cf_score}
            )
        # sort: if cf_score exists, by cf_score desc, otherwise keep ontology order
        results_sorted = sorted(
            results,
            key=lambda r: (
                r["cf_score"] is not None,
                r["cf_score"] if r["cf_score"] is not None else 0,
            ),
            reverse=True,
        )
        return results_sorted[:top_k]
