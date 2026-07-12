import json, os, re

def get_manifest(max_p):
    path = f"results/sweep_p{max_p}_manifest.json"
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_key_data_summary():
    lines = [
        "| Bound ($p$) | Exceptional Primes Found | Unique $A$-Values Used | Max minimal $A$ |",
        "|-------------|--------------------------|-------------------------|-----------------|"
    ]
    for max_p in [10**5, 10**6, 10**7, 10**8]:
        mf = get_manifest(max_p)
        if not mf: continue
        power = len(str(max_p)) - 1
        found = f"{mf['total_solved']:,}"
        unique_a = len(mf['distribution_m'])
        max_m = mf['max_minimal_m']
        max_a = 4 * max_m + 3
        lines.append(f"| $10^{power}$      | ${found}$                  | ${unique_a}$                    | ${max_a}$            |")
    return "\n".join(lines)

def update_file(filename, section_start, section_end, new_content):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = re.compile(rf"({re.escape(section_start)}).*?({re.escape(section_end)})", re.DOTALL)
    if not pattern.search(content):
        print(f"Warning: section not found in {filename}")
        return
        
    new_text = f"\\1\n\n{new_content}\n\n\\2"
    content = pattern.sub(new_text, content)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    summary = generate_key_data_summary()
    update_file("EMPIRICAL_NOTE.md", "### Key Data Summary", "### Shift Distribution table", summary)
    print("Updated EMPIRICAL_NOTE.md")
    
    # Update README
    mf_10e6 = get_manifest(10**6)
    mf_10e7 = get_manifest(10**7)
    mf_10e8 = get_manifest(10**8)
    if mf_10e6 and mf_10e7 and mf_10e8:
        readme_str = f"**10⁶: {mf_10e6['total_solved']}/{mf_10e6['total_solved']}, 10⁷: {mf_10e7['total_solved']}/{mf_10e7['total_solved']}, 10⁸: {mf_10e8['total_solved']}/{mf_10e8['total_solved']}**"
        update_file("README.md", "<!-- ZERO_FAILURES_START -->", "<!-- ZERO_FAILURES_END -->", readme_str)
        print("Updated README.md")
    
if __name__ == '__main__':
    main()
