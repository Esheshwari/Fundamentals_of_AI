"""
Family Tree Inference System
Using Forward Chaining and Backward Chaining
"""

# ─────────────────────────────────────────────
# KNOWLEDGE BASE
# ─────────────────────────────────────────────

facts = set()       # stores base facts as tuples e.g. ('parent', 'tom', 'bob')
inferred = set()    # stores forward-chained inferred facts


def add_fact(*fact):
    facts.add(fact)


def is_fact(rel, a, b=None):
    if b:
        return (rel, a, b) in facts or (rel, a, b) in inferred
    return (rel, a) in facts or (rel, a) in inferred


# ─────────────────────────────────────────────
# FORWARD CHAINING ENGINE
# ─────────────────────────────────────────────

def forward_chain():
    """
    Apply all inference rules repeatedly until no new facts are derived.
    Populates the `inferred` set with derived relationships.
    """
    changed = True
    while changed:
        changed = False
        people = get_all_people()

        for a in people:
            for b in people:
                if a == b:
                    continue

                # Rule: grandparent(X,Z) :- parent(X,Y), parent(Y,Z)
                for c in people:
                    if c == a or c == b:
                        continue
                    if is_fact('parent', a, b) and is_fact('parent', b, c):
                        if ('grandparent', a, c) not in inferred:
                            inferred.add(('grandparent', a, c))
                            changed = True

                    # Rule: great_grandparent(X,Z) :- grandparent(X,Y), parent(Y,Z)
                    if is_fact('grandparent', a, b) and is_fact('parent', b, c):
                        if ('great_grandparent', a, c) not in inferred:
                            inferred.add(('great_grandparent', a, c))
                            changed = True

                    # Rule: sibling(X,Z) :- parent(Y,X), parent(Y,Z), X!=Z
                    if is_fact('parent', a, b) and is_fact('parent', a, c):
                        if ('sibling', b, c) not in inferred and b != c:
                            inferred.add(('sibling', b, c))
                            changed = True
                        if ('sibling', c, b) not in inferred and b != c:
                            inferred.add(('sibling', c, b))
                            changed = True

                # Rule: child(X,Y) :- parent(Y,X)
                if is_fact('parent', b, a):
                    if ('child', a, b) not in inferred:
                        inferred.add(('child', a, b))
                        changed = True

                # Rule: ancestor(X,Y) :- parent(X,Y)
                if is_fact('parent', a, b):
                    if ('ancestor', a, b) not in inferred:
                        inferred.add(('ancestor', a, b))
                        changed = True

                # Rule: ancestor(X,Z) :- ancestor(X,Y), parent(Y,Z)
                for c in people:
                    if c == a or c == b:
                        continue
                    if is_fact('ancestor', a, b) and is_fact('parent', b, c):
                        if ('ancestor', a, c) not in inferred:
                            inferred.add(('ancestor', a, c))
                            changed = True

        # Gender-based rules
        for a in people:
            for b in people:
                if a == b:
                    continue

                # father / mother
                if is_fact('parent', a, b):
                    if is_fact('male', a):
                        if ('father', a, b) not in inferred:
                            inferred.add(('father', a, b))
                            changed = True
                    if is_fact('female', a):
                        if ('mother', a, b) not in inferred:
                            inferred.add(('mother', a, b))
                            changed = True

                # son / daughter
                if is_fact('child', a, b):
                    if is_fact('male', a):
                        if ('son', a, b) not in inferred:
                            inferred.add(('son', a, b))
                            changed = True
                    if is_fact('female', a):
                        if ('daughter', a, b) not in inferred:
                            inferred.add(('daughter', a, b))
                            changed = True

                # grandfather / grandmother
                if is_fact('grandparent', a, b):
                    if is_fact('male', a):
                        if ('grandfather', a, b) not in inferred:
                            inferred.add(('grandfather', a, b))
                            changed = True
                    if is_fact('female', a):
                        if ('grandmother', a, b) not in inferred:
                            inferred.add(('grandmother', a, b))
                            changed = True

                # brother / sister
                if is_fact('sibling', a, b):
                    if is_fact('male', a):
                        if ('brother', a, b) not in inferred:
                            inferred.add(('brother', a, b))
                            changed = True
                    if is_fact('female', a):
                        if ('sister', a, b) not in inferred:
                            inferred.add(('sister', a, b))
                            changed = True

                # uncle / aunt :- sibling(S, Parent) and parent(Parent, X)
                for c in people:
                    if c in (a, b):
                        continue
                    if is_fact('sibling', a, c) and is_fact('parent', c, b):
                        if is_fact('male', a):
                            if ('uncle', a, b) not in inferred:
                                inferred.add(('uncle', a, b))
                                changed = True
                        if is_fact('female', a):
                            if ('aunt', a, b) not in inferred:
                                inferred.add(('aunt', a, b))
                                changed = True

                    # nephew / niece :- sibling(X, Parent) and parent(Parent, Y)
                    if is_fact('sibling', b, c) and is_fact('parent', c, a):
                        if is_fact('male', a):
                            if ('nephew', a, b) not in inferred:
                                inferred.add(('nephew', a, b))
                                changed = True
                        if is_fact('female', a):
                            if ('niece', a, b) not in inferred:
                                inferred.add(('niece', a, b))
                                changed = True

                    # great_uncle / great_aunt
                    if is_fact('sibling', a, c) and is_fact('grandparent', c, b):
                        if is_fact('male', a):
                            if ('great_uncle', a, b) not in inferred:
                                inferred.add(('great_uncle', a, b))
                                changed = True
                        if is_fact('female', a):
                            if ('great_aunt', a, b) not in inferred:
                                inferred.add(('great_aunt', a, b))
                                changed = True

                    # cousin :- parent(P1, X), parent(P2, Y), sibling(P1, P2)
                    for d in people:
                        if d in (a, b, c):
                            continue
                        if (is_fact('parent', c, a) and is_fact('parent', d, b)
                                and is_fact('sibling', c, d)):
                            if ('cousin', a, b) not in inferred:
                                inferred.add(('cousin', a, b))
                                changed = True
                            if ('cousin', b, a) not in inferred:
                                inferred.add(('cousin', b, a))
                                changed = True

                        # second_cousin :- parent(P1,X), parent(P2,Y), cousin(P1,P2)
                        if (is_fact('parent', c, a) and is_fact('parent', d, b)
                                and is_fact('cousin', c, d)):
                            if ('second_cousin', a, b) not in inferred:
                                inferred.add(('second_cousin', a, b))
                                changed = True
                            if ('second_cousin', b, a) not in inferred:
                                inferred.add(('second_cousin', b, a))
                                changed = True

                # spouse symmetry
                if is_fact('spouse', a, b):
                    if ('spouse', b, a) not in inferred and ('spouse', b, a) not in facts:
                        inferred.add(('spouse', b, a))
                        changed = True

                # in-law rules
                for c in people:
                    if c in (a, b):
                        continue
                    # mother_in_law / father_in_law
                    if is_fact('spouse', a, c) and is_fact('parent', b, c):
                        if is_fact('female', b):
                            if ('mother_in_law', b, a) not in inferred:
                                inferred.add(('mother_in_law', b, a))
                                changed = True
                        if is_fact('male', b):
                            if ('father_in_law', b, a) not in inferred:
                                inferred.add(('father_in_law', b, a))
                                changed = True

                    # sibling_in_law
                    if is_fact('spouse', a, c) and is_fact('sibling', b, c):
                        if ('sibling_in_law', b, a) not in inferred:
                            inferred.add(('sibling_in_law', b, a))
                            changed = True


# ─────────────────────────────────────────────
# BACKWARD CHAINING ENGINE
# ─────────────────────────────────────────────

def backward_chain(goal_rel, x, y, visited=None, depth=0):
    """
    Try to prove (goal_rel, x, y) using backward chaining.
    Returns (bool, explanation_steps_list).
    """
    if visited is None:
        visited = set()

    indent = "  " * depth
    goal = (goal_rel, x, y)

    if goal in visited:
        return False, []
    visited.add(goal)

    # Check base facts
    if goal in facts:
        return True, [f"{indent}✔ Base fact: {x} {goal_rel} {y}"]

    # Check already inferred facts
    if goal in inferred:
        return True, [f"{indent}✔ Inferred: {x} {goal_rel} {y}"]

    people = get_all_people()
    steps = []

    # ── RULES (backward) ──

    if goal_rel == 'grandparent':
        # grandparent(X,Z) :- parent(X,Y), parent(Y,Z)
        for mid in people:
            if mid in (x, y):
                continue
            ok1, s1 = backward_chain('parent', x, mid, visited.copy(), depth+1)
            ok2, s2 = backward_chain('parent', mid, y, visited.copy(), depth+1)
            if ok1 and ok2:
                return True, [f"{indent}→ Rule: grandparent via {mid}"] + s1 + s2

    elif goal_rel == 'great_grandparent':
        for mid in people:
            if mid in (x, y):
                continue
            ok1, s1 = backward_chain('grandparent', x, mid, visited.copy(), depth+1)
            ok2, s2 = backward_chain('parent', mid, y, visited.copy(), depth+1)
            if ok1 and ok2:
                return True, [f"{indent}→ Rule: great_grandparent via {mid}"] + s1 + s2

    elif goal_rel == 'sibling':
        for parent in people:
            if parent in (x, y):
                continue
            ok1, s1 = backward_chain('parent', parent, x, visited.copy(), depth+1)
            ok2, s2 = backward_chain('parent', parent, y, visited.copy(), depth+1)
            if ok1 and ok2:
                return True, [f"{indent}→ Rule: sibling via shared parent {parent}"] + s1 + s2

    elif goal_rel == 'brother':
        ok1, s1 = backward_chain('sibling', x, y, visited.copy(), depth+1)
        ok2, s2 = backward_chain('male', x, x, visited.copy(), depth+1)
        if ok1 and ok2:
            return True, [f"{indent}→ Rule: brother = male sibling"] + s1 + s2

    elif goal_rel == 'sister':
        ok1, s1 = backward_chain('sibling', x, y, visited.copy(), depth+1)
        ok2, s2 = backward_chain('female', x, x, visited.copy(), depth+1)
        if ok1 and ok2:
            return True, [f"{indent}→ Rule: sister = female sibling"] + s1 + s2

    elif goal_rel == 'father':
        ok1, s1 = backward_chain('parent', x, y, visited.copy(), depth+1)
        ok2, s2 = backward_chain('male', x, x, visited.copy(), depth+1)
        if ok1 and ok2:
            return True, [f"{indent}→ Rule: father = male parent"] + s1 + s2

    elif goal_rel == 'mother':
        ok1, s1 = backward_chain('parent', x, y, visited.copy(), depth+1)
        ok2, s2 = backward_chain('female', x, x, visited.copy(), depth+1)
        if ok1 and ok2:
            return True, [f"{indent}→ Rule: mother = female parent"] + s1 + s2

    elif goal_rel == 'son':
        ok1, s1 = backward_chain('parent', y, x, visited.copy(), depth+1)
        ok2, s2 = backward_chain('male', x, x, visited.copy(), depth+1)
        if ok1 and ok2:
            return True, [f"{indent}→ Rule: son = male child"] + s1 + s2

    elif goal_rel == 'daughter':
        ok1, s1 = backward_chain('parent', y, x, visited.copy(), depth+1)
        ok2, s2 = backward_chain('female', x, x, visited.copy(), depth+1)
        if ok1 and ok2:
            return True, [f"{indent}→ Rule: daughter = female child"] + s1 + s2

    elif goal_rel == 'grandfather':
        ok1, s1 = backward_chain('grandparent', x, y, visited.copy(), depth+1)
        ok2, s2 = backward_chain('male', x, x, visited.copy(), depth+1)
        if ok1 and ok2:
            return True, [f"{indent}→ Rule: grandfather = male grandparent"] + s1 + s2

    elif goal_rel == 'grandmother':
        ok1, s1 = backward_chain('grandparent', x, y, visited.copy(), depth+1)
        ok2, s2 = backward_chain('female', x, x, visited.copy(), depth+1)
        if ok1 and ok2:
            return True, [f"{indent}→ Rule: grandmother = female grandparent"] + s1 + s2

    elif goal_rel == 'uncle':
        for parent in people:
            if parent in (x, y):
                continue
            ok1, s1 = backward_chain('sibling', x, parent, visited.copy(), depth+1)
            ok2, s2 = backward_chain('parent', parent, y, visited.copy(), depth+1)
            ok3, s3 = backward_chain('male', x, x, visited.copy(), depth+1)
            if ok1 and ok2 and ok3:
                return True, [f"{indent}→ Rule: uncle via {parent}"] + s1 + s2 + s3

    elif goal_rel == 'aunt':
        for parent in people:
            if parent in (x, y):
                continue
            ok1, s1 = backward_chain('sibling', x, parent, visited.copy(), depth+1)
            ok2, s2 = backward_chain('parent', parent, y, visited.copy(), depth+1)
            ok3, s3 = backward_chain('female', x, x, visited.copy(), depth+1)
            if ok1 and ok2 and ok3:
                return True, [f"{indent}→ Rule: aunt via {parent}"] + s1 + s2 + s3

    elif goal_rel == 'nephew':
        for parent in people:
            if parent in (x, y):
                continue
            ok1, s1 = backward_chain('sibling', y, parent, visited.copy(), depth+1)
            ok2, s2 = backward_chain('parent', parent, x, visited.copy(), depth+1)
            ok3, s3 = backward_chain('male', x, x, visited.copy(), depth+1)
            if ok1 and ok2 and ok3:
                return True, [f"{indent}→ Rule: nephew via {parent}"] + s1 + s2 + s3

    elif goal_rel == 'niece':
        for parent in people:
            if parent in (x, y):
                continue
            ok1, s1 = backward_chain('sibling', y, parent, visited.copy(), depth+1)
            ok2, s2 = backward_chain('parent', parent, x, visited.copy(), depth+1)
            ok3, s3 = backward_chain('female', x, x, visited.copy(), depth+1)
            if ok1 and ok2 and ok3:
                return True, [f"{indent}→ Rule: niece via {parent}"] + s1 + s2 + s3

    elif goal_rel == 'cousin':
        for p1 in people:
            for p2 in people:
                if len({x, y, p1, p2}) < 4:
                    continue
                ok1, s1 = backward_chain('parent', p1, x, visited.copy(), depth+1)
                ok2, s2 = backward_chain('parent', p2, y, visited.copy(), depth+1)
                ok3, s3 = backward_chain('sibling', p1, p2, visited.copy(), depth+1)
                if ok1 and ok2 and ok3:
                    return True, [f"{indent}→ Rule: cousin via parents {p1} & {p2}"] + s1 + s2 + s3

    elif goal_rel == 'second_cousin':
        for p1 in people:
            for p2 in people:
                if len({x, y, p1, p2}) < 4:
                    continue
                ok1, s1 = backward_chain('parent', p1, x, visited.copy(), depth+1)
                ok2, s2 = backward_chain('parent', p2, y, visited.copy(), depth+1)
                ok3, s3 = backward_chain('cousin', p1, p2, visited.copy(), depth+1)
                if ok1 and ok2 and ok3:
                    return True, [f"{indent}→ Rule: second_cousin via {p1} & {p2}"] + s1 + s2 + s3

    elif goal_rel == 'great_uncle':
        for parent in people:
            if parent in (x, y):
                continue
            ok1, s1 = backward_chain('sibling', x, parent, visited.copy(), depth+1)
            ok2, s2 = backward_chain('grandparent', parent, y, visited.copy(), depth+1)
            ok3, s3 = backward_chain('male', x, x, visited.copy(), depth+1)
            if ok1 and ok2 and ok3:
                return True, [f"{indent}→ Rule: great_uncle via {parent}"] + s1 + s2 + s3

    elif goal_rel == 'great_aunt':
        for parent in people:
            if parent in (x, y):
                continue
            ok1, s1 = backward_chain('sibling', x, parent, visited.copy(), depth+1)
            ok2, s2 = backward_chain('grandparent', parent, y, visited.copy(), depth+1)
            ok3, s3 = backward_chain('female', x, x, visited.copy(), depth+1)
            if ok1 and ok2 and ok3:
                return True, [f"{indent}→ Rule: great_aunt via {parent}"] + s1 + s2 + s3

    elif goal_rel == 'ancestor':
        ok1, s1 = backward_chain('parent', x, y, visited.copy(), depth+1)
        if ok1:
            return True, [f"{indent}→ Rule: direct ancestor"] + s1
        for mid in people:
            if mid in (x, y):
                continue
            ok1, s1 = backward_chain('ancestor', x, mid, visited.copy(), depth+1)
            ok2, s2 = backward_chain('parent', mid, y, visited.copy(), depth+1)
            if ok1 and ok2:
                return True, [f"{indent}→ Rule: ancestor chain via {mid}"] + s1 + s2

    elif goal_rel == 'spouse':
        if ('spouse', y, x) in facts or ('spouse', y, x) in inferred:
            return True, [f"{indent}✔ Spouse (symmetric): {y} spouse {x}"]

    elif goal_rel in ('male', 'female'):
        if (goal_rel, x) in facts:
            return True, [f"{indent}✔ Base fact: {x} is {goal_rel}"]

    return False, [f"{indent}✘ Cannot prove: {x} {goal_rel} {y}"]


# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────

def get_all_people():
    people = set()
    for f in facts | inferred:
        if len(f) == 3:
            people.add(f[1])
            people.add(f[2])
        elif len(f) == 2:
            people.add(f[1])
    return people


def query(relation, person_a, person_b):
    """Query a relationship using both forward and backward chaining."""
    print(f"\n{'='*60}")
    print(f"  QUERY: Is {person_a} the {relation} of {person_b}?")
    print(f"{'='*60}")

    # Forward chaining check
    forward_chain()
    in_inferred = (relation, person_a, person_b) in inferred
    in_facts = (relation, person_a, person_b) in facts

    print(f"\n[FORWARD CHAINING]")
    if in_facts:
        print(f"  ✔ TRUE  — found as a base fact.")
    elif in_inferred:
        print(f"  ✔ TRUE  — derived by forward chaining rules.")
    else:
        print(f"  ✘ Not found in forward-chained facts.")

    # Backward chaining check
    print(f"\n[BACKWARD CHAINING]")
    result, chain = backward_chain(relation, person_a, person_b)
    if result:
        print(f"  ✔ TRUE  — proved by backward chaining.")
    else:
        print(f"  ✘ FALSE — could not prove.")
    print(f"\n  Reasoning chain:")
    for step in chain:
        print(f"    {step}")

    answer = result or in_inferred or in_facts
    print(f"\n  FINAL ANSWER: {'✔ YES' if answer else '✘ NO'}")
    print(f"{'='*60}")
    return answer


def show_all_facts():
    print("\n── BASE FACTS ──────────────────────────────")
    if not facts:
        print("  (none)")
    for f in sorted(facts):
        if len(f) == 3:
            print(f"  {f[1]} → [{f[0]}] → {f[2]}")
        else:
            print(f"  {f[1]} is {f[0]}")


def show_inferred():
    forward_chain()
    print("\n── INFERRED FACTS ──────────────────────────")
    if not inferred:
        print("  (none)")
    for f in sorted(inferred):
        if len(f) == 3:
            print(f"  {f[1]} → [{f[0]}] → {f[2]}")
        else:
            print(f"  {f[1]} is {f[0]}")


# ─────────────────────────────────────────────
# MAIN DEMO
# ─────────────────────────────────────────────

if __name__ == "__main__":

    print("╔══════════════════════════════════════════════╗")
    print("║   FAMILY TREE INFERENCE SYSTEM               ║")
    print("║   Forward Chaining + Backward Chaining       ║")
    print("╚══════════════════════════════════════════════╝")

    # ── Assert base facts ──
    # Generation 1 (great-grandparents)
    add_fact('male',   'george')
    add_fact('female', 'helen')
    add_fact('parent', 'george', 'tom')
    add_fact('parent', 'george', 'mary')
    add_fact('parent', 'helen',  'tom')
    add_fact('parent', 'helen',  'mary')
    add_fact('spouse', 'george', 'helen')

    # Generation 2 (grandparents)
    add_fact('male',   'tom')
    add_fact('female', 'mary')
    add_fact('female', 'sue')
    add_fact('male',   'peter')
    add_fact('spouse', 'tom',   'sue')
    add_fact('spouse', 'peter', 'mary')

    add_fact('parent', 'tom',   'bob')
    add_fact('parent', 'sue',   'bob')
    add_fact('parent', 'tom',   'liz')
    add_fact('parent', 'sue',   'liz')
    add_fact('parent', 'mary',  'ann')
    add_fact('parent', 'peter', 'ann')
    add_fact('parent', 'mary',  'pat')
    add_fact('parent', 'peter', 'pat')

    # Generation 3 (parents)
    add_fact('male',   'bob')
    add_fact('female', 'liz')
    add_fact('female', 'ann')
    add_fact('male',   'pat')

    add_fact('parent', 'bob',  'jim')
    add_fact('parent', 'bob',  'amy')
    add_fact('parent', 'ann',  'clara')

    # Generation 4 (children)
    add_fact('male',   'jim')
    add_fact('female', 'amy')
    add_fact('female', 'clara')

    # ── Show base facts ──
    show_all_facts()

    # ── Run forward chaining and show inferred ──
    forward_chain()
    show_inferred()

    # ── Queries ──
    print("\n\n══════════════════════════════════════════════")
    print("  RUNNING QUERIES")
    print("══════════════════════════════════════════════")

    query('father',          'tom',    'bob')
    query('grandmother',     'sue',    'jim')
    query('grandfather',     'george', 'bob')
    query('sibling',         'bob',    'liz')
    query('brother',         'bob',    'liz')
    query('sister',          'liz',    'bob')
    query('cousin',          'jim',    'clara')
    query('second_cousin',   'jim',    'clara')   # should be False
    query('uncle',           'pat',    'jim')
    query('aunt',            'liz',    'jim')
    query('great_grandparent', 'george', 'jim')
    query('ancestor',        'george', 'jim')
    query('great_aunt',      'mary',   'jim')

    # ── Interactive mode ──
    print("\n\n══════════════════════════════════════════════")
    print("  INTERACTIVE QUERY MODE  (type 'exit' to quit)")
    print("══════════════════════════════════════════════")
    print("  People in tree:", sorted(get_all_people()))
    print("""
  Supported relations:
  parent, child, father, mother, son, daughter,
  sibling, brother, sister, grandparent, grandfather,
  grandmother, great_grandparent, ancestor, uncle, aunt,
  nephew, niece, great_uncle, great_aunt, cousin,
  second_cousin, spouse
    """)

    while True:
        try:
            rel = input("Relation (or 'exit'): ").strip().lower()
            if rel == 'exit':
                break
            a = input("Person A: ").strip().lower()
            b = input("Person B: ").strip().lower()
            query(rel, a, b)
        except (KeyboardInterrupt, EOFError):
            break

    print("\nGoodbye!")
