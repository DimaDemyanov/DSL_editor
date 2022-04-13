import React from 'react';
import AceEditor from "react-ace";

export function SourceCode(props) {
  return (
        <AceEditor
          width="100%"
          height="100%"
          placeholder="Placeholder Text"
          mode="java"
          theme="github"
          name="SourceCode"
          fontSize={14}
          showPrintMargin={false}
          showGutter={true}
          highlightActiveLine={true}
          // maxLines="Infinity"
          value={props.value}
          ref={props.fRef}
          onLoad={() => console.log('loaded')}
          setOptions={{
          enableBasicAutocompletion: false,
          enableLiveAutocompletion: false,
          enableSnippets: false,
          showLineNumbers: true,
          tabSize: 2
          }}/>
      )
}
