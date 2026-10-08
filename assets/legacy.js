---
layout: null
---
(() => {
  const projects = {
    {% assign separator = '' %}{% for item in site.data.projects %}{% if item[1].legacy_id %}{{ separator }}"portfolioModal-{{ item[1].legacy_id }}": {{ '/projects/' | append: item[0] | append: '/' | relative_url | jsonify }}{% assign separator = ',' %}
    {% endif %}{% endfor %}
  };
  function followLegacyLink() {
    const key = window.location.hash.slice(1);
    if (Object.prototype.hasOwnProperty.call(projects, key)) window.location.replace(projects[key]);
  }
  followLegacyLink();
  window.addEventListener('hashchange', followLegacyLink);
})();
