"""Discover changes in bounded directed routes between shared concepts."""
from collections import deque
from copy import deepcopy
import html
import re


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


def discover_stories(before, after, cutoff=5, limit=30):
    old, new = shortest_routes(before, cutoff), shortest_routes(after, cutoff)
    shared = {n['id'] for n in before['nodes']} & {n['id'] for n in after['nodes']}
    old_edges = {(e['from'], e['to']) for e in before['edges']}
    new_edges = {(e['from'], e['to']) for e in after['edges']}
    stories = []
    for start, end in sorted(old.keys() | new.keys()):
        if start not in shared or end not in shared:
            continue
        earlier, later = old.get((start, end)), new.get((start, end))
        if earlier == later or max(len(earlier or ()), len(later or ())) < 3:
            continue
        removed = path_edges(earlier) - new_edges
        added = path_edges(later) - old_edges
        # Ignore a different tie-breaking choice among otherwise unchanged routes.
        if not removed and not added:
            continue
        kind = 'New bounded route' if not earlier else 'Lost bounded route' if not later else 'Changed route'
        stories.append(dict(start=start, end=end, earlier=earlier, later=later,
                            kind=kind, added=added, removed=removed))
    stories.sort(key=lambda s: (-(len(s['added']) + len(s['removed'])),
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
    stories = discover_stories(before, after, cutoff)
    st.caption('Breadth-first search chooses one shortest directed path per endpoint pair. Suggestions prioritize changed connections and include paths of at least two edges. This is a bounded comparison, not an exhaustive search of alternative routes. Snapshot sidebar filters do not apply here.')
    if not stories:
        st.info('No changed routes found within this path limit. Try another age, year pair, or limit.')
        return
    index = st.selectbox('Suggested story', range(len(stories)),
                         format_func=lambda i: f"{stories[i]['kind']}: {stories[i]['start']} → {stories[i]['end']}",
                         key=f'story_choice_{age}_{earlier}_{later}_{cutoff}')
    story = stories[index]
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
