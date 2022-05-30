const initialise = function() {
    $('input[name="text"]').on('keypress', () => $('.has-error').hide());
};
