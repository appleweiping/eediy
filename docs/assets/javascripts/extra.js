(() => {
  "use strict";

  const storagePrefix = "eediy:check:";
  const mobileNavigationQuery = "(max-width: 76.234375em)";
  let teardown = () => {};

  const safeStorage = {
    get(key) {
      try {
        return window.localStorage.getItem(key);
      } catch (_error) {
        return null;
      }
    },
    set(key, value) {
      try {
        window.localStorage.setItem(key, value);
      } catch (_error) {
        // Persistence is optional in private or restricted browsing modes.
      }
    },
    remove(key) {
      try {
        window.localStorage.removeItem(key);
      } catch (_error) {
        // See set().
      }
    }
  };

  function pageKey() {
    return window.location.pathname.replace(/\/+$/, "") || "/";
  }

  function isEnglishPage() {
    return /(^|\/)en(\/|$)/.test(window.location.pathname);
  }

  function setupDocumentLanguage() {
    document.documentElement.lang = isEnglishPage() ? "en" : "zh-Hans";
  }

  function setupLocalizedPermalinks() {
    const label = isEnglishPage() ? "Permanent link" : "永久链接";
    document.querySelectorAll("a.headerlink").forEach((link) => {
      link.title = label;
      link.setAttribute("aria-label", label);
    });
  }

  function setupSkipLink() {
    const article = document.querySelector(".md-content__inner");
    const skipLink = document.querySelector("[data-md-component='skip'] .md-skip");
    if (!article || !skipLink) return;

    article.id = "ee-main-content";
    article.tabIndex = -1;
    skipLink.href = "#ee-main-content";
    skipLink.textContent = isEnglishPage()
      ? "Skip to main content"
      : "跳到主要内容";
    skipLink.setAttribute("aria-label", skipLink.textContent);
  }

  function directNavigationTitle(item) {
    const directElement = Array.from(item.children).find((child) =>
      child.matches?.(".md-nav__container, .md-nav__link")
    );
    return directElement?.querySelector(".md-ellipsis")?.textContent.trim()
      || directElement?.textContent.trim()
      || "";
  }

  function makeToggleAccessible(labels, input, panel, getLabel, signal) {
    if (!input || !panel || labels.length === 0) {
      return { sync: () => {}, trigger: null };
    }

    if (!panel.id) {
      panel.id = `ee-panel-${input.id.replace(/^_+/, "")}`;
    }

    const trigger = labels.find((label) => !panel.contains(label)) || labels[0];
    labels.forEach((label) => {
      label.tabIndex = 0;
      label.setAttribute("role", "button");
      label.setAttribute("aria-controls", panel.id);
      label.addEventListener("keydown", (event) => {
        if (event.key !== "Enter" && event.key !== " ") return;
        event.preventDefault();
        input.click();
      }, { signal });
    });

    const sync = () => {
      labels.forEach((label) => {
        const text = getLabel(input.checked);
        label.setAttribute("aria-expanded", String(input.checked));
        label.setAttribute("aria-label", text);
        label.title = text;
      });
    };
    input.addEventListener("change", sync, { signal });
    sync();
    return { sync, trigger };
  }

  function setPanelFocusability(panel, hidden, fallback) {
    if (!panel) return;
    if (hidden && panel.contains(document.activeElement) && fallback) {
      fallback.focus();
    }
    panel.toggleAttribute("inert", hidden);
    if (hidden) {
      panel.setAttribute("aria-hidden", "true");
    } else {
      panel.removeAttribute("aria-hidden");
    }
  }

  function setupNavigationAndSearch(signal) {
    const english = isEnglishPage();
    const mobile = window.matchMedia(mobileNavigationQuery);
    const drawer = document.getElementById("__drawer");
    const drawerPanel = document.querySelector(".md-sidebar--primary");
    const drawerControl = makeToggleAccessible(
      Array.from(document.querySelectorAll(
        "label.md-header__button[for='__drawer']"
      )),
      drawer,
      drawerPanel,
      (expanded) => english
        ? `${expanded ? "Close" : "Open"} navigation`
        : `${expanded ? "关闭" : "打开"}导航`,
      signal
    );

    const search = document.getElementById("__search");
    const searchPanel = document.querySelector(
      ".md-search[data-md-component='search']"
    );
    const searchLabels = Array.from(document.querySelectorAll(
      "label.md-header__button[for='__search'], label.md-search__icon[for='__search']"
    ));
    searchLabels.forEach((label) => label.setAttribute("aria-haspopup", "dialog"));
    const searchControl = makeToggleAccessible(
      searchLabels,
      search,
      searchPanel,
      (expanded) => english
        ? `${expanded ? "Close" : "Open"} search`
        : `${expanded ? "关闭" : "打开"}搜索`,
      signal
    );

    const nestedControls = [];
    document.querySelectorAll(
      ".md-sidebar--primary input.md-nav__toggle[id^='__nav_']"
    ).forEach((input) => {
      const item = input.closest(".md-nav__item");
      if (!item) return;
      const panel = Array.from(item.children).find((child) =>
        child.matches?.("nav.md-nav")
      );
      const labels = Array.from(document.querySelectorAll(`label[for='${input.id}']`));
      if (!panel || labels.length === 0) return;
      const title = directNavigationTitle(item) || (english ? "section" : "分组");
      const control = makeToggleAccessible(
        labels,
        input,
        panel,
        (expanded) => english
          ? `${expanded ? "Collapse" : "Expand"} ${title}`
          : `${expanded ? "收起" : "展开"}${title}`,
        signal
      );
      nestedControls.push({ input, panel, control });
    });

    const sync = () => {
      drawerControl.sync();
      searchControl.sync();
      setPanelFocusability(
        drawerPanel,
        Boolean(drawer && mobile.matches && !drawer.checked),
        drawerControl.trigger
      );
      setPanelFocusability(
        searchPanel,
        Boolean(search && mobile.matches && !search.checked),
        searchControl.trigger
      );
      nestedControls.forEach(({ input, panel, control }) => {
        control.sync();
        setPanelFocusability(panel, mobile.matches && !input.checked, control.trigger);
      });
    };

    drawer?.addEventListener("change", sync, { signal });
    search?.addEventListener("change", sync, { signal });
    nestedControls.forEach(({ input }) => {
      input.addEventListener("change", sync, { signal });
    });
    mobile.addEventListener("change", sync);
    signal.addEventListener("abort", () => {
      mobile.removeEventListener("change", sync);
    }, { once: true });
    sync();
  }

  function setupLanguageScopedSearch(signal) {
    const result = document.querySelector(
      "[data-md-component='search-result']"
    );
    const resultList = result?.querySelector(".md-search-result__list");
    if (!result || !resultList) return;

    const english = isEnglishPage();
    result.dataset.eeSearchLanguage = english ? "en" : "zh";
    resultList.setAttribute(
      "aria-label",
      english ? "Search results in English" : "中文搜索结果"
    );
  }

  function setupChecklists(signal) {
    document.querySelectorAll("ul.task-list").forEach((list) => {
      list.querySelectorAll(
        ":scope > .task-list-item > .task-list-control > input[type='checkbox']"
      ).forEach((box, index) => {
        const label = box.closest(".task-list-item")?.textContent.trim();
        box.disabled = false;
        box.dataset.eeCheck ||= `markdown-${index}`;
        if (label) {
          box.setAttribute("aria-label", label);
          box.title = label;
        }
      });
    });

    document.querySelectorAll(".ee-checklist, ul.task-list").forEach(
      (checklist, listIndex) => {
        const boxes = Array.from(
          checklist.querySelectorAll("input[data-ee-check]")
        );
        const counter = checklist.querySelector(".ee-check-progress");
        const reset = checklist.querySelector(".ee-reset-progress");
        const scope = `${storagePrefix}${pageKey()}:${listIndex}:`;

        const updateCounter = () => {
          if (!counter) return;
          const completed = boxes.filter((box) => box.checked).length;
          const completeLabel = counter.dataset.completeLabel || "Complete";
          const ofLabel = counter.dataset.ofLabel || "of";
          counter.textContent = `${completeLabel} ${completed} ${ofLabel} ${boxes.length}`;
        };

        if (counter) {
          counter.setAttribute("role", "status");
          counter.setAttribute("aria-live", "polite");
          counter.setAttribute("aria-atomic", "true");
        }

        boxes.forEach((box, boxIndex) => {
          const identity = box.dataset.eeCheck || String(boxIndex);
          const key = `${scope}${identity}`;
          box.checked = safeStorage.get(key) === "1";
          box.addEventListener("change", () => {
            safeStorage.set(key, box.checked ? "1" : "0");
            updateCounter();
          }, { signal });
        });

        reset?.addEventListener("click", () => {
          boxes.forEach((box, boxIndex) => {
            const identity = box.dataset.eeCheck || String(boxIndex);
            safeStorage.remove(`${scope}${identity}`);
            box.checked = false;
          });
          updateCounter();
        }, { signal });
        updateCounter();
      }
    );
  }

  function improveScrollableTables(signal) {
    const tables = Array.from(document.querySelectorAll(".md-content table"));
    const wrappers = tables.map((table) => {
      let wrapper = table.parentElement?.matches(".md-typeset__table")
        ? table.parentElement
        : null;
      if (!wrapper) {
        wrapper = document.createElement("div");
        wrapper.className = "md-typeset__table";
        table.before(wrapper);
        wrapper.append(table);
      }
      table.removeAttribute("tabindex");
      return wrapper;
    });

    const update = () => {
      wrappers.forEach((wrapper, index) => {
        const overflow = wrapper.scrollWidth > wrapper.clientWidth + 1;
        wrapper.toggleAttribute("data-ee-overflow", overflow);
        if (overflow) {
          wrapper.tabIndex = 0;
          wrapper.setAttribute("role", "region");
          wrapper.setAttribute(
            "aria-label",
            isEnglishPage()
              ? `Scrollable data table ${index + 1}`
              : `可横向滚动的数据表 ${index + 1}`
          );
        } else {
          wrapper.removeAttribute("tabindex");
          wrapper.removeAttribute("role");
          wrapper.removeAttribute("aria-label");
        }
      });
    };

    const observer = "ResizeObserver" in window ? new ResizeObserver(update) : null;
    wrappers.forEach((wrapper) => observer?.observe(wrapper));
    tables.forEach((table) => observer?.observe(table));
    signal.addEventListener("abort", () => observer?.disconnect(), { once: true });
    window.addEventListener("resize", update, { passive: true, signal });
    update();
  }

  function initialize() {
    teardown();
    const controller = new AbortController();
    teardown = () => controller.abort();
    setupDocumentLanguage();
    setupLocalizedPermalinks();
    setupSkipLink();
    setupNavigationAndSearch(controller.signal);
    setupLanguageScopedSearch(controller.signal);
    setupChecklists(controller.signal);
    improveScrollableTables(controller.signal);
    document.documentElement.dataset.eeReady = "true";
  }

  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(initialize);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialize, { once: true });
  } else {
    initialize();
  }
})();
