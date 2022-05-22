export default (state) => {
    return ({
        style: state ? {background: '#FFFFFF'} : {background: '#A9A9A9'},
        readOnly: !state,
        highlightActiveLine: state
    })
}
