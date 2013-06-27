"""Controllers for twittertorss app."""

from django import shortcuts
from django.views.generic import edit


class CreateView(edit.CreateView):
  """Basic controller for creating objects."""

  def get(self, request):
    """Process a get request."""
    return shortcuts.render(
        request, self.template_name, {'form': self.form_class()})

  def post(self, request):
    """Process a post submission."""
    form = self.form_class(request.POST)
    # If the form is valid, save the corresponding model and redirect.
    if form.is_valid():
      model = self.model(**form.cleaned_data)
      model.put()
      return shortcuts.redirect(self.success_url)

    # Form isn't valid, so display the template with the form.
    else:
      return shortcuts.render(request, self.template_name, {'form': form})


class DeleteView(edit.DeleteView):
  """Basic controller for deleting objects."""

  def post(self, request, slug=None):
    """Process a post submission."""
    model = self.model.query(getattr(self.model, self.slug_field) == slug).get()
    model.key.delete()
    return shortcuts.redirect(self.success_url)
