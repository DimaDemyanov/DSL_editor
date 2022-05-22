export default (state) => ({
    style: state ? {background: '#FFFFFF'} : {background: '#A9A9A9'},
    readOnly: !state,
    highlightActiveLine: state
})
