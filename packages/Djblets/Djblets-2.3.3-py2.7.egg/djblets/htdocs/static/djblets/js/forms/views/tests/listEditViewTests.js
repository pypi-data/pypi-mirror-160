"use strict";

suite('djblets/forms/views/ListEditView', function () {
  /*
   * See templates/djblets_forms/list_edit_widget.html.
   */
  const formTemplate = _.template("<div class=\"djblets-c-list-edit-widget\">\n <ul class=\"djblets-c-list-edit-widget__entries\">\n  <% if (items.length > 0) { %>\n   <% items.forEach(function(item, i) { %>\n    <li class=\"djblets-c-list-edit-widget__entry\"\n        data-list-index=\"<%- i %>\">\n     <input value=\"<%- item %>\" type=\"text\"<%= attrs %>>\n     <a href=\"#\" class=\"djblets-c-list-edit-widget__remove-item\"></a>\n    </li>\n   <% }); %>\n  <% } else { %>\n   <li class=\"djblets-c-list-edit-widget__entry\" data-list-index=\"0\">\n    <input type=\"text\">\n    <a href=\"#\" class=\"djblets-c-list-edit-widget__remove-item\"></a>\n   </li>\n  <% } %>\n </ul>\n <button class=\"djblets-c-list-edit-widget__add-item\"></button>\n <input class=\"djblets-c-list-edit-widget__value\"\n        type=\"hidden\" value=\"<%- nonZeroItems.join(',') %>\">\n</div>");

  const makeView = function makeView() {
    let items = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : [];
    let attrs = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : '';
    attrs = attrs.length ? " ".concat(attrs) : '';
    attrs = "".concat(attrs, " class=\"djblets-c-list-edit-widget__input\"");
    const $el = $(formTemplate({
      items: items,
      nonZeroItems: items.filter(i => i.length > 0),
      attrs: attrs
    })).appendTo($testsScratch);
    const view = new Djblets.Forms.ListEditView({
      el: $el,
      inputAttrs: attrs,
      sep: ','
    });
    view.render();
    return [view, view.$('.djblets-c-list-edit-widget__value')];
  };

  describe('Updating fields', function () {
    it('With no values', function () {
      const [, $valueField] = makeView([]);
      expect($valueField.val()).toEqual('');
    });
    it('With one value', function () {
      const [view, $valueField] = makeView(['One']);
      expect($valueField.val()).toEqual('One');
      view.$('.djblets-c-list-edit-widget__input').val('Foo').blur();
      expect($valueField.val()).toEqual('Foo');
    });
    it('With multiple values', function () {
      const [view, $valueField] = makeView(['one', 'two', 'three']);
      const $inputs = view.$('.djblets-c-list-edit-widget__input');
      expect($valueField.val()).toEqual('one,two,three');
      $inputs.eq(2).val('baz').blur();
      expect($valueField.val()).toEqual('one,two,baz');
      $inputs.eq(0).val('').blur();
      expect($valueField.val()).toEqual('two,baz');
      $inputs.eq(1).val('').blur();
      expect($valueField.val()).toEqual('baz');
      $inputs.eq(2).val('').blur();
      expect($valueField.val()).toEqual('');
    });
  });
  describe('Removal', function () {
    it('With no values', function () {
      const [view, $valueField] = makeView([]);
      expect($valueField.val()).toEqual('');
      expect(view.$('.djblets-c-list-edit-widget__entry').length).toEqual(1);
      view.$('.djblets-c-list-edit-widget__remove-item').click();
      expect($valueField.val()).toEqual('');
      expect(view.$('.djblets-c-list-edit-widget__entry').length).toEqual(1);
    });
    it('With one value', function () {
      const [view, $valueField] = makeView(['One']);
      expect($valueField.val()).toEqual('One');
      view.$('.djblets-c-list-edit-widget__remove-item').click();
      expect($valueField.val()).toEqual('');
      expect(view.$('.djblets-c-list-edit-widget__entry').length).toEqual(1);
    });
    it('With multiple values', function () {
      const [view, $valueField] = makeView(['One', 'Two', 'Three']);
      expect($valueField.val()).toEqual('One,Two,Three');
      expect(view.$('.djblets-c-list-edit-widget__remove-item').length).toEqual(3);
      view.$('.djblets-c-list-edit-widget__remove-item').eq(1).click();
      expect($valueField.val()).toEqual('One,Three');
      expect(view.$('.djblets-c-list-edit-widget__entry').length).toEqual(2);
      expect(view.$('.djblets-c-list-edit-widget__remove-item').length).toEqual(2);
      view.$('.djblets-c-list-edit-widget__remove-item').eq(1).click();
      expect($valueField.val()).toEqual('One');
      expect(view.$('.djblets-c-list-edit-widget__entry').length).toEqual(1);
      expect(view.$('.djblets-c-list-edit-widget__remove-item').length).toEqual(1);
      view.$('.djblets-c-list-edit-widget__remove-item').click();
      expect($valueField.val()).toEqual('');
      expect(view.$('.djblets-c-list-edit-widget__entry').length).toEqual(1);
    });
  });
  describe('Addition', function () {
    it('With values', function () {
      const [view, $valueField] = makeView(['one', 'two', 'three']);
      expect($valueField.val()).toEqual('one,two,three');
      view.$('.djblets-c-list-edit-widget__add-item').click();
      expect($valueField.val()).toEqual('one,two,three');
      expect(view.$('.djblets-c-list-edit-widget__entry').length).toEqual(4);
      view.$('.djblets-c-list-edit-widget__input').eq(3).val('four').blur();
      expect($valueField.val()).toEqual('one,two,three,four');
    });
    it('With blank values', function () {
      const [view, $valueField] = makeView(['', '', '']);
      expect($valueField.val()).toEqual('');
      view.$('.djblets-c-list-edit-widget__add-item').click();
      expect($valueField.val()).toEqual('');
      expect(view.$('.djblets-c-list-edit-widget__entry').length).toEqual(4);
      view.$('.djblets-c-list-edit-widget__input').eq(3).val('four').blur();
      expect($valueField.val()).toEqual('four');
    });
    it('With correct attributes', function () {
      const [view] = makeView([], 'size="100" readonly');
      view.$('.djblets-c-list-edit-widget__add-item').click();
      const $input = view.$('input').eq(1);
      expect($input.attr('size')).toEqual('100');
      expect($input.prop('readonly')).toBe(true);
    });
  });
});

//# sourceMappingURL=listEditViewTests.js.map