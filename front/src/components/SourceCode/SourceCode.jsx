import React from 'react';
import AceEditor from 'react-ace';

export function SourceCode(props) {
  return (
    <AceEditor
      className={props.className}
      style={props.style}
      width="100%"
      height="100%"
      placeholder="Placeholder Text"
      mode="java"
      theme="github"
      name="SourceCode"
      fontSize={14}
      showPrintMargin={false}
      showGutter
      highlightActiveLine={props.highlightActiveLine}
      readOnly={props.readOnly ? props.readOnly : false}
      // maxLines="Infinity"
      value={props.value}
      ref={props.fRef}
      onLoad={() => console.log('Editor is loaded')}
      setOptions={{
        enableBasicAutocompletion: false,
        enableLiveAutocompletion: false,
        enableSnippets: false,
        showLineNumbers: true,
        tabSize: 2,
      }}
    />
  );
}
