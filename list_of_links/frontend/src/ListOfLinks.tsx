import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"
import "./index.css"

interface State {
  selectedLinkTarget: string
}

class ListOfLinks extends StreamlitComponentBase<State> {
  public state = { selectedLinkTarget: "" }

  constructor(props: any) {
    super(props)
    // Set defaultLink to state when component is initialized
    this.state = { selectedLinkTarget: this.props.args["default"] || "" }
  }

  public render = (): ReactNode => {
    // Arguments that are passed to the plugin in Python are accessible
    // via `this.props.args`. Here, we access the "name" arg.
    const title = this.props.args["title"]
    const links = this.props.args["links"]

    const listItems = links.map((link: [string, string]) => (
      <li key={`${link[1]}`}>
        <a
          href={`#${link[1]}`}
          className={`group flex gap-x-3 rounded-md p-2 text-sm font-semibold leading-6 hover:bg-gray-800 hover:text-white ${this.state.selectedLinkTarget === link[1] ? "bg-gray-400 text-white" : "text-gray-400"}`}
          onClick={() => this.onClicked(link[1])}
        >
          <span className={"text-truncate"}>
            {link[0]}
          </span>
        </a>
      </li>
    ))

    return (
      <span>
        <h3 className={"text-xs font-semibold leading-6 text-gray-400"}>{title}</h3>
        <ul className={"mt-2 space-y-1"}>{listItems}</ul>
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
