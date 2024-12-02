import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"

interface State {
  selectedLinkTarget: string
}

class ListOfLinks extends StreamlitComponentBase<State> {
  public state = { selectedLinkTarget: "" }

  public render = (): ReactNode => {
    // Arguments that are passed to the plugin in Python are accessible
    // via `this.props.args`. Here, we access the "name" arg.
    const title = this.props.args["title"]
    const links = this.props.args["links"]

    const listItems = links.map((link: [string, string]) => (
      <li key={`${link[1]}`}
          style={{ backgroundColor: this.state.selectedLinkTarget === link[1] ? "lightgray" : "transparent" }}>
        <a
          href={`#${link[1]}`}
          onClick={() => this.onClicked(link[1])}
        >
          {link[0]}
        </a>
      </li>
    ))

    return (
      <span>
        <h3>{title}</h3>
        <ul>{listItems}</ul>
      </span>
    )
  }

  private onClicked = (linkTarget: string) => {
    // Function to send the linkTarget back to Streamlit
    this.setState(
      () => ({ selectedLinkTarget: linkTarget }),
      () => Streamlit.setComponentValue(this.state.selectedLinkTarget)
    )
  }
}

export default withStreamlitConnection(ListOfLinks)
