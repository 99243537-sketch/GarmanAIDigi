/*
 * AIDigi 数据加载器
 * 读取 data/ 目录下的 CSV 文件，交给页面里的图表和表格绘制。
 * 新增一份数据：把 CSV 放进 data/，再在下面 SOURCES 里加一行。
 */
(function () {
  var SOURCES = {
    users: 'data/ai_users.csv',
    growth: 'data/ai_growth.csv',
    funding: 'data/ai_funding.csv',
    capex: 'data/ai_capex.csv',
    compute: 'data/ai_compute.csv',
    marketcap: 'data/ai_marketcap.csv'
  };

  // 图表系列颜色，浅色和深色背景下都清晰可辨
  var COLORS = ['#3b7dd8', '#d9822b', '#2e9e6b', '#9b59b6', '#c7444a', '#1aa3a3', '#b8860b', '#7a7a7a'];

  var store = {};
  var draws = [];

  function runDraws() {
    draws.forEach(function (d) {
      document.querySelectorAll('[data-draw="' + d.name + '"]').forEach(function (el) {
        try { d.fn(el); } catch (e) { console.error('绘制 ' + d.name + ' 出错：', e); }
      });
    });
  }

  window.dash = {
    colors: COLORS,
    data: function (id) {
      return store[id] || { status: 'loading', data: [] };
    },
    draw: function (name, fn) {
      draws.push({ name: name, fn: fn });
    }
  };

  function load() {
    var jobs = Object.keys(SOURCES).map(function (id) {
      return fetch(SOURCES[id], { cache: 'no-cache' })
        .then(function (r) {
          if (!r.ok) throw new Error(r.status + ' ' + SOURCES[id]);
          return r.text();
        })
        .then(function (text) {
          var rows = d3.csvParse(text.replace(/^﻿/, ''));
          store[id] = { status: 'ok', data: rows, columns: rows.columns };
        })
        .catch(function (e) {
          console.error('数据加载失败：', e);
          store[id] = { status: 'error', data: [], message: String(e) };
        });
    });
    Promise.all(jobs).then(runDraws);
  }

  var timer = null;
  window.addEventListener('resize', function () {
    clearTimeout(timer);
    timer = setTimeout(runDraws, 150);
  });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { runDraws(); load(); });
  } else {
    setTimeout(function () { runDraws(); load(); }, 0);
  }
})();
