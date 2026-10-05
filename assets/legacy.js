---
layout: null
---
(() => {
  const projects = {
    {% for item in site.data.projects %}"portfolioModal-{{ item[1].legacy_id }}": {{ '/projects/' | append: item[0] | append: '/' | relative_url | jsonify }}{% unless forloop.last %},{% endunless %}
    {% endfor %}
  };
  function followLegacyLink() {
    const key = window.location.hash.slice(1);
    if (Object.prototype.hasOwnProperty.call(projects, key)) window.location.replace(projects[key]);
  }
  followLegacyLink();
  window.addEventListener('hashchange', followLegacyLink);
})();
