"""Discover changes in bounded directed routes between shared concepts."""
from collections import deque
from copy import deepcopy
import html
import re
import networkx as nx


def story_paragraph(story, before, after, cutoff):
    """A narrative frame grounded in route nodes and original edge explanations."""
    age = before['age']
    person = f'a child aged {age}' if age < 18 else f'an adult aged {age}'
    paths = [story['earlier'], story['later']]

    def describe(snapshot, path):
        if not path:
            return (f"The {snapshot['year']} graph does not show a connecting route within "
                    f"{cutoff} edges. ")
        edges = {(edge['from'], edge['to']): edge for edge in snapshot['edges']}
        sentences = []
        for source, target in zip(path, path[1:]):
            title = html.unescape(re.sub(r'<[^>]+>', ' ', edges[source, target].get('title', '')))
            match = re.search(r'Why:\s*(.*?)(?=\s*Strength:|$)', title, re.S)
            explanation = (' '.join(match.group(1).split()).rstrip('. ')
                           if match else f'{source} is linked to {target}')
            # Preserve names, acronyms, and the source explanation's uncertainty.
            sentences.append(explanation + '.')
        return ' '.join(sentences) + ' '

    text = (f"For {person}, the relationship between {story['start']} and "
            f"{story['end']} takes a different shape in these two snapshots. ")
    if paths[0]:
        text += f"In {before['year']}, the connection unfolds through the following influences: "
    text += describe(before, paths[0])
    if paths[1]:
        text += f"By comparison, the {after['year']} snapshot follows a different route. "
    text += describe(after, paths[1])
    if all(paths):
        old_middle, new_middle = paths[0][1:-1], paths[1][1:-1]
        earlier_link = ', '.join(old_middle) if old_middle else 'a direct link'
        later_link = ', '.join(new_middle) if new_middle else 'a direct link'
        text += (f"Where the earlier account connects these conditions through {earlier_link}, "
                 f"the later account brings {later_link} into focus. "
                 f"What changes is the set of influences surrounding the person, "
                 f"and how those influences connect to {story['end']}.")
    elif paths[1]:
        text += ('The later snapshot therefore gives this relationship a visible chain of influences '
                 'that the earlier view does not capture within the selected path length.')
    else:
        text += ('The earlier chain is no longer visible within the selected path length in the later '
                 'snapshot; that absence does not establish that the relationship itself has disappeared.')
    return text



def shortest_routes(snapshot, cutoff=5):
    """BFS gives one deterministic shortest simple route per reachable pair."""
    nodes = {node['id'] for node in snapshot['nodes']}
    adjacency = {node: set() for node in nodes}
    for edge in snapshot['edges']:
        if edge['from'] in nodes and edge['to'] in nodes:
            adjacency[edge['from']].add(edge['to'])
    routes = {}
    for start in sorted(nodes):
        queue = deque([(start,)])
        seen = {start}
        while queue:
            path = queue.popleft()
            if len(path) - 1 >= cutoff:
                continue
            for target in sorted(adjacency[path[-1]]):
                if target in seen:
                    continue
                seen.add(target)
                route = path + (target,)
                routes[start, target] = route
                queue.append(route)
    return routes


def path_edges(path):
    return set(zip(path, path[1:])) if path else set()


def alternative_routes(snapshot, cutoff=5, count=4):
    """Yen's algorithm returns up to k shortest simple directed paths per pair."""
    graph = nx.DiGraph()
    graph.add_nodes_from(sorted(n['id'] for n in snapshot['nodes']))
    nodes = set(graph)
    graph.add_edges_from(sorted((e['from'], e['to']) for e in snapshot['edges']
                               if e['from'] in nodes and e['to'] in nodes))
    routes = {}
    # BFS determines exact bounded reachability before alternative enumeration.
    for start, end in shortest_routes(snapshot, cutoff):
        paths = []
        for path in nx.shortest_simple_paths(graph, start, end):
            if len(path) - 1 > cutoff:
                break
            paths.append(tuple(path))
            if len(paths) >= count:
                break
        routes[start, end] = paths
    return routes


def domain_transitions(snapshot, path):
    groups = snapshot.get('node_groups', {})
    ignored = {'unknown', 'factor', None, ''}
    transitions = set()
    for a, b in zip(path or (), (path or ())[1:]):
        left, right = groups.get(a), groups.get(b)
        if left not in ignored and right not in ignored and left != right:
            transitions.add((left, right))
    return transitions


def rank_change(earlier, later, before, after, added, removed):
    """Transparent structural heuristic, not an evidence or causal score."""
    def distance(a, b):
        return len(a ^ b) / len(a | b) if a or b else 0.0
    old_domains = domain_transitions(before, earlier)
    new_domains = domain_transitions(after, later)
    edge_change = len(added | removed) / max(1, len(path_edges(earlier) | path_edges(later)))
    concept_change = distance(set((earlier or ())[1:-1]), set((later or ())[1:-1]))
    domain_change = distance(old_domains, new_domains)
    cross_domain = min(len(old_domains | new_domains) / 3, 1.0)
    score = 100 * (0.45 * edge_change + 0.30 * concept_change
                   + 0.20 * domain_change + 0.05 * cross_domain)
    return round(score, 2), old_domains, new_domains


def discover_stories(before, after, cutoff=5, limit=30):
    old, new = alternative_routes(before, cutoff), alternative_routes(after, cutoff)
    shared = {n['id'] for n in before['nodes']} & {n['id'] for n in after['nodes']}
    old_edges = {(e['from'], e['to']) for e in before['edges']}
    new_edges = {(e['from'], e['to']) for e in after['edges']}
    stories = []
    for start, end in sorted(old.keys() | new.keys()):
        if start not in shared or end not in shared:
            continue
        candidates = []
        for earlier in old.get((start, end), [None]):
            for later in new.get((start, end), [None]):
                if earlier == later or max(len(earlier or ()), len(later or ())) < 3:
                    continue
                removed = path_edges(earlier) - new_edges
                added = path_edges(later) - old_edges
                # Different alternatives alone are not a historical graph change.
                if not removed and not added:
                    continue
                score, old_domains, new_domains = rank_change(earlier, later, before, after, added, removed)
                kind = 'New bounded route' if not earlier else 'Lost bounded route' if not later else 'Changed route'
                candidates.append(dict(start=start, end=end, earlier=earlier, later=later,
                                       kind=kind, added=added, removed=removed, score=score,
                                       old_domains=old_domains, new_domains=new_domains,
                                       alternatives_before=len(old.get((start, end), [])),
                                       alternatives_after=len(new.get((start, end), []))))
        candidates.sort(key=lambda s: (-s['score'], len(s['earlier'] or ()) + len(s['later'] or ()),
                                      s['earlier'] or (), s['later'] or ()))
        # One representative per endpoint pair avoids flooding the dropdown.
        if candidates:
            stories.append(candidates[0])
    stories.sort(key=lambda s: (-s['score'],
                               max(len(s['earlier'] or ()), len(s['later'] or ())),
                               s['start'], s['end']))
    return stories[:limit]


def highlight_path(snapshot, path):
    highlighted = deepcopy(snapshot)
    selected_nodes = set(path or ())
    selected_edges = path_edges(path)
    for node in highlighted['nodes']:
        if node['id'] in selected_nodes:
            node.update(borderWidth=4, borderWidthSelected=5)
        else:
            node.update(opacity=0.18, font={'color': '#cbd5e1'})
    for edge in highlighted['edges']:
        if (edge['from'], edge['to']) in selected_edges:
            edge.update(width=5)
        else:
            edge.update(color={'color': '#d1d5db', 'opacity': 0.16}, width=1,
                        title='', label='')
    return highlighted


def render_story_paths(snapshots, build_html):
    import streamlit as st
    import streamlit.components.v1 as components

    st.markdown('### Story paths')
    st.caption('Automatically discovered changes between shared concepts. Paths follow edge direction; no endpoints need to be selected.')
    controls = st.columns(4)
    ages = sorted({age for values in snapshots.values() for age in values})
    age = controls[0].selectbox('Story age', ages, key='story_age')
    years = sorted(y for y in snapshots if age in snapshots[y])
    if len(years) < 2:
        st.info('Two snapshots of this age are needed.')
        return
    earlier = controls[1].selectbox('Earlier year', years[:-1],
                                    index=years[:-1].index(1990) if 1990 in years[:-1] else 0,
                                    key='story_earlier')
    later_years = [year for year in years if year > earlier]
    later = controls[2].selectbox('Later year', later_years, index=len(later_years)-1,
                                 key='story_later')
    cutoff = controls[3].slider('Maximum edges per path', 2, 7, 5, key='story_cutoff')
    before, after = snapshots[earlier][age], snapshots[later][age]
    stories = st.cache_data(show_spinner='Finding alternative story paths…')(discover_stories)(before, after, cutoff)
    st.caption('Compares up to four shortest simple directed paths per endpoint pair in each year. Suggestions favor changed connections, intermediate concepts, and transitions across domains. One representative comparison per endpoint pair is shown, up to 30 stories. Snapshot sidebar filters do not apply here.')
    if not stories:
        st.info('No changed routes found within this path limit. Try another age, year pair, or limit.')
        return
    index = st.selectbox('Suggested story', range(len(stories)),
                         format_func=lambda i: f"{stories[i]['kind']}: {stories[i]['start']} → {stories[i]['end']}",
                         key=f'story_choice_{age}_{earlier}_{later}_{cutoff}')
    story = stories[index]
    with st.expander('Why this story is suggested'):
        st.write(f"Alternatives compared: {story['alternatives_before']} in {earlier}, {story['alternatives_after']} in {later}.")
        st.write('Ranking weights: changed connections 45%, changed intermediate concepts 30%, changed domain transitions 20%, cross-domain breadth 5%. This is a structural storytelling heuristic, not a measure of evidence or causal importance.')
        st.write(f"Comparison score: {story['score']:.1f}/100. Among the sampled alternatives, the highest-scoring pair is displayed; other routes may still persist.")
        for year, domains in [(earlier, story['old_domains']), (later, story['new_domains'])]:
            st.write(f"{year} domain transitions: " + ('; '.join(f'{a} → {b}' for a, b in sorted(domains)) or 'No labeled cross-domain transitions'))
    for col, snapshot, path in zip(st.columns(2), (before, after), (story['earlier'], story['later'])):
        with col:
            st.markdown(f"#### {snapshot['year']} · Age {age}")
            if path:
                st.write(' → '.join(path))
            else:
                st.info(f'No directed path found within {cutoff} edges.')
            display = highlight_path(snapshot, path)
            graph_html = build_html(display, 0.0, 510)
            components.html(graph_html, height=545, scrolling=False)
    st.markdown('#### What changed?')
    st.write(story_paragraph(story, before, after, cutoff))
    st.caption('Based on original graph explanations. The years compare people of the same age, not one person aging; these are model relationships, not a personal case history.')
    with st.expander('See the graph changes behind the story'):
        for label, edges in [('Connections on the later path absent from the earlier graph', story['added']),
                         ('Connections on the earlier path absent from the later graph', story['removed'])]:
            if edges:
                st.write(label + ': ' + '; '.join(f'{a} → {b}' for a, b in sorted(edges)))
    st.caption('These stories describe the snapshots, not when mechanisms first appeared in the world. Evidence for individual edges does not establish a causal effect for the full path. Bold edges and outlined nodes mark the selected route; other elements remain as context.')
