import streamlit as st
from explain import explain_code

st.set_page_config(page_title="CodeExplain", page_icon="📝", layout="wide")
st.title("📝 CodeExplain")
st.subheader("Natural Language Code Documentation Generator")
st.write("Paste Python source code and generate human-readable documentation.")

sample = """def calculate_sum(a, b):
    result = a + b
    return result

class Calculator:
    def multiply(self, x, y):
        return x * y
"""
left, right = st.columns(2)
with left:
    st.markdown("### Source code")
    code = st.text_area("Paste your code", value=sample, height=420)
    run = st.button("🚀 Generate Documentation", type="primary", use_container_width=True)
with right:
    st.markdown("### Generated documentation")
    if run:
        if not code.strip():
            st.warning("Please enter code first.")
        else:
            result = explain_code(code)
            st.success("Analysis completed")
            st.markdown("#### Summary")
            st.write(result["summary"])
            if result["imports"]:
                st.markdown("#### Imported modules")
                st.write(", ".join(result["imports"]))
            if result["functions"]:
                st.markdown("#### Functions")
                for f in result["functions"]:
                    with st.expander(f'{f["name"]}() — line {f["line"]}'):
                        st.write("Parameters: " + (", ".join(f["args"]) or "None"))
                        st.write("Docstring: " + f["docstring"])
            if result["classes"]:
                st.markdown("#### Classes")
                for c in result["classes"]:
                    st.write(f'**{c["name"]}** — methods: {", ".join(c["methods"]) or "None"}')
            if result["complexity"] is not None:
                st.metric("Approximate cyclomatic complexity", result["complexity"])
            st.markdown("#### Line-by-line explanation")
            for item in result["details"]:
                st.write("• " + item)
            md = "# CodeExplain Documentation\n\n## Summary\n" + result["summary"] + "\n\n## Details\n" + "\n".join("- "+x for x in result["details"])
            st.download_button("⬇️ Download Markdown report", md, "code_documentation.md", "text/markdown")
    else:
        st.info("Enter code and click Generate Documentation.")
st.divider()
st.caption("Prototype: Python AST + keyword/pattern analysis + rule-based natural-language generation.")
