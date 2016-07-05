

QUnit.test("hides error test", function (assert) {
    assert.equal($('.has-error').is(':visible'), true);
    $('.has-error').hide();
    assert.equal($('.has-error').is(':visible'), false);
});

QUnit.test("hides error test 2", function (assert) {
    assert.equal($('.has-error').is(':visible'), true);
    $('.has-error').hide();
    assert.equal($('.has-error').is(':visible'), false);
});

QUnit.test("errors hidden on keypress", function (assert) {
    $('input').trigger('keypress');
    assert.equal($('.has-error').is(':visible'), false);
});

QUnit.test("errors not hidden unless keypress", function (assert) {
    assert.equal($('.has-error').is(':visible'), true);
});
