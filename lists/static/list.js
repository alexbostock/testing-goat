window.SuperLists = {
    initialise() {
        $('input[name="text"]').on('keypress', () => $('.has-error').hide());
    }
};
