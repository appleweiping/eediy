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
        // Progress persistence is optional; the page remains fully usable.
      }
    },
    remove(key) {
      try {
        window.localStorage.removeItem(key);
      } catch (_error) {
        // See set(): storage may be unavailable in private or restricted modes.
      }
    }
  };

  function pageKey() {
    return window.location.pathname.replace(/\/+$/, "") || "/";
  }

  function isEnglishPage() {
    return /(^|\/)en(\/|$)/.test(window.location.pathname);
  }

  function setDocumentLanguage() {
    document.documentElement.lang = isEnglishPage() ? "en" : "zh-Hans";
  }

  function setupSkipLink() {
    const article = document.querySelector(".md-content__inner");
    const skipLink = document.querySelector("[data-md-component='skip'] .md-skip");
    if (!article || !skipLink) return;

    // Material's default target is the first heading, which can skip the home-page
    // hero. A stable main-content target works on every instant-navigation page.
    article.id = "ee-main-content";
    article.tabIndex = -1;
    skipLink.href = "#ee-main-content";
    skipLink.textContent = isEnglishPage()
      ? "Skip to main content"
      : "跳到主要内容";
    skipLink.setAttribute("aria-label", skipLink.textContent);
  }

  function setupHeaderLanguageSwitch() {
    const header = document.querySelector(".md-header__inner");
    if (!header) return;

    const logo = header.querySelector("a.md-header__button.md-logo");
    const baseUrl = logo
      ? new URL(logo.href, window.location.href)
      : new URL("./", window.location.href);
    const basePath = baseUrl.pathname.endsWith("/")
      ? baseUrl.pathname
      : `${baseUrl.pathname}/`;
    const currentPath = window.location.pathname.startsWith(basePath)
      ? window.location.pathname.slice(basePath.length)
      : window.location.pathname.replace(/^\/+/, "");
    const isEnglish = currentPath === "en" || currentPath.startsWith("en/");
    const counterpartPath = isEnglish
      ? currentPath.replace(/^en\/?/, "")
      : `en/${currentPath}`;
    const target = new URL(`${basePath}${counterpartPath}`, window.location.origin);
    // Keep deep-link state when moving between the bilingual page pair.
    target.search = window.location.search;
    target.hash = window.location.hash;

    let link = header.querySelector(".ee-header-language");
    if (!link) {
      link = document.createElement("a");
      link.className = "md-header__button ee-header-language";
      const searchToggle = header.querySelector("label[for='__search']");
      if (searchToggle) {
        searchToggle.before(link);
      } else {
        header.append(link);
      }
    }

    link.href = target.href;
    link.hreflang = isEnglish ? "zh-Hans" : "en";
    link.lang = isEnglish ? "zh-Hans" : "en";
    link.textContent = isEnglish ? "中" : "EN";
    link.title = isEnglish ? "切换到简体中文" : "Switch to English";
    link.setAttribute("aria-label", link.title);
  }

  function makeToggleLabelsAccessible(labels, input, panel, getLabel, signal) {
    if (!input || !panel || labels.length === 0) {
      return { sync: () => {}, externalLabel: null };
    }

    if (!panel.id) {
      panel.id = `ee-panel-${input.id.replace(/^_+/, "")}`;
    }

    const externalLabel = labels.find((label) => !panel.contains(label)) || labels[0];

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
        const accessibleLabel = getLabel(input.checked, label);
        label.setAttribute("aria-expanded", String(input.checked));
        label.setAttribute("aria-label", accessibleLabel);
        label.title = accessibleLabel;
      });
    };

    input.addEventListener("change", sync, { signal });
    sync();
    return { sync, externalLabel };
  }

  function setPanelFocusability(panel, hidden, fallback) {
    if (!panel) return;

    if (hidden && panel.contains(document.activeElement) && fallback) {
      fallback.focus();
    }

    // `inert` removes every descendant from sequential focus without rewriting
    // Material's own tabindex values, so reopening restores native behavior.
    panel.toggleAttribute("inert", hidden);
    if (hidden) {
      panel.setAttribute("aria-hidden", "true");
    } else {
      panel.removeAttribute("aria-hidden");
    }
  }

  function setupNavigationAndSearch(signal) {
    const isEnglish = isEnglishPage();
    const mobile = window.matchMedia(mobileNavigationQuery);
    const drawer = document.getElementById("__drawer");
    const drawerPanel = document.querySelector(".md-sidebar--primary");
    const drawerLabels = Array.from(
      document.querySelectorAll("label.md-header__button[for='__drawer']")
    );
    const drawerToggle = makeToggleLabelsAccessible(
      drawerLabels,
      drawer,
      drawerPanel,
      (expanded) => {
        if (isEnglish) return expanded ? "Close navigation" : "Open navigation";
        return expanded ? "关闭导航" : "打开导航";
      },
      signal
    );

    const search = document.getElementById("__search");
    const searchPanel = document.querySelector(".md-search[data-md-component='search']");
    const searchLabels = Array.from(document.querySelectorAll(
      "label.md-header__button[for='__search'], label.md-search__icon[for='__search']"
    ));
    const searchToggle = makeToggleLabelsAccessible(
      searchLabels,
      search,
      searchPanel,
      (expanded) => {
        if (isEnglish) return expanded ? "Close search" : "Open search";
        return expanded ? "关闭搜索" : "打开搜索";
      },
      signal
    );
    searchLabels.forEach((label) => label.setAttribute("aria-haspopup", "dialog"));

    const nestedToggles = [];
    document.querySelectorAll(
      ".md-sidebar--primary input.md-nav__toggle[id^='__nav_']"
    ).forEach((input) => {
      const item = input.closest(".md-nav__item");
      const panel = item
        ? Array.from(item.children).find((child) => child.matches?.("nav.md-nav"))
        : null;
      const labels = Array.from(
        document.querySelectorAll(`label[for='${input.id}']`)
      );
      if (!panel || labels.length === 0) return;

      const title = (
        item.querySelector(":scope > .md-nav__container .md-ellipsis")
        || item.querySelector(":scope > label.md-nav__link .md-ellipsis")
        || labels.find((label) => label.textContent.trim())
      )?.textContent.trim() || (isEnglish ? "section" : "分组");

      const toggle = makeToggleLabelsAccessible(
        labels,
        input,
        panel,
        (expanded) => {
          if (isEnglish) return `${expanded ? "Collapse" : "Expand"} ${title}`;
          return `${expanded ? "收起" : "展开"}${title}`;
        },
        signal
      );
      nestedToggles.push({ input, panel, toggle });
    });

    const syncFocusability = () => {
      drawerToggle.sync();
      searchToggle.sync();
      setPanelFocusability(
        drawerPanel,
        Boolean(drawer && mobile.matches && !drawer.checked),
        drawerToggle.externalLabel
      );
      setPanelFocusability(
        searchPanel,
        Boolean(search && mobile.matches && !search.checked),
        searchToggle.externalLabel
      );

      nestedToggles.forEach(({ input, panel, toggle }) => {
        toggle.sync();
        setPanelFocusability(
          panel,
          mobile.matches && !input.checked,
          toggle.externalLabel
        );
      });
    };

    drawer?.addEventListener("change", syncFocusability, { signal });
    search?.addEventListener("change", syncFocusability, { signal });
    nestedToggles.forEach(({ input }) => {
      input.addEventListener("change", syncFocusability, { signal });
    });
    mobile.addEventListener("change", syncFocusability);
    signal.addEventListener("abort", () => {
      mobile.removeEventListener("change", syncFocusability);
    }, { once: true });
    syncFocusability();
  }

  function setupReadingProgress(signal) {
    let bar = document.querySelector(".ee-reading-progress");
    if (!bar) {
      bar = document.createElement("div");
      bar.className = "ee-reading-progress";
      bar.setAttribute("role", "progressbar");
      bar.setAttribute("aria-valuemin", "0");
      bar.setAttribute("aria-valuemax", "100");
      document.body.prepend(bar);
    }

    const update = () => {
      const article = document.querySelector(".md-content__inner");
      const isEnglish = isEnglishPage();
      if (!article) {
        bar.hidden = true;
        return;
      }

      const start = article.getBoundingClientRect().top + window.scrollY;
      const documentEnd = Math.max(
        document.documentElement.scrollHeight - window.innerHeight,
        0
      );
      const articleEnd = Math.min(
        start + article.offsetHeight - window.innerHeight,
        documentEnd
      );
      const distance = articleEnd - start;
      const isScrollable = distance > 1;
      bar.hidden = !isScrollable;
      if (!isScrollable) return;

      const progress = Math.min(Math.max((window.scrollY - start) / distance, 0), 1);
      const percentage = Math.round(progress * 100);
      bar.style.transform = `scaleX(${progress})`;
      bar.setAttribute("aria-label", isEnglish ? "Reading progress" : "阅读进度");
      bar.setAttribute("aria-valuenow", String(percentage));
      bar.setAttribute(
        "aria-valuetext",
        isEnglish ? `${percentage}% read` : `已阅读 ${percentage}%`
      );
    };

    update();
    window.addEventListener("scroll", update, { passive: true, signal });
    window.addEventListener("resize", update, { passive: true, signal });
  }

  function setupChecklists(signal) {
    // Pymdown renders Markdown task-list text outside the visual checkbox label.
    // Promote those lists to the same persistent checklist behavior and give
    // every control an explicit accessible name derived from its list item.
    document.querySelectorAll("ul.task-list").forEach((list) => {
      list.classList.add("ee-checklist");
      list.querySelectorAll(
        ":scope > .task-list-item > .task-list-control > input[type='checkbox']"
      ).forEach((box, boxIndex) => {
        const item = box.closest(".task-list-item");
        const label = item?.textContent.trim();
        box.disabled = false;
        box.dataset.eeCheck ||= `markdown-${boxIndex}`;
        if (label) {
          box.setAttribute("aria-label", label);
          box.title = label;
        }
      });
    });

    document.querySelectorAll(".ee-checklist").forEach((checklist, listIndex) => {
      const boxes = Array.from(checklist.querySelectorAll("input[data-ee-check]"));
      const counter = checklist.querySelector(".ee-check-progress");
      const reset = checklist.querySelector(".ee-reset-progress");
      const scope = `${storagePrefix}${pageKey()}:${listIndex}:`;

      if (counter) {
        // Announce persisted and user-triggered progress as one atomic sentence.
        counter.setAttribute("role", "status");
        counter.setAttribute("aria-live", "polite");
        counter.setAttribute("aria-atomic", "true");
      }

      const updateCounter = () => {
        if (!counter) return;
        const completed = boxes.filter((box) => box.checked).length;
        const completeLabel = counter.dataset.completeLabel || "Complete";
        const ofLabel = counter.dataset.ofLabel || "of";
        counter.textContent = `${completeLabel} ${completed} ${ofLabel} ${boxes.length}`;
      };

      boxes.forEach((box, boxIndex) => {
        const identity = box.dataset.eeCheck || String(boxIndex);
        const key = `${scope}${identity}`;
        box.checked = safeStorage.get(key) === "1";
        box.addEventListener("change", () => {
          safeStorage.set(key, box.checked ? "1" : "0");
          updateCounter();
        }, { signal });
      });

      if (reset) {
        reset.addEventListener("click", () => {
          boxes.forEach((box, boxIndex) => {
            const identity = box.dataset.eeCheck || String(boxIndex);
            safeStorage.remove(`${scope}${identity}`);
            box.checked = false;
          });
          updateCounter();
        }, { signal });
      }

      updateCounter();
    });
  }

  function improveScrollableTables(signal) {
    const tables = Array.from(
      document.querySelectorAll(".md-content .md-typeset table")
    );
    const wrappers = tables.map((table) => {
      let wrapper = table.parentElement?.matches(".md-typeset__table")
        ? table.parentElement
        : null;

      // Plain Markdown tables are not always wrapped by Material. The wrapper is
      // the real overflow owner and therefore the correct keyboard focus target.
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
        const hasHorizontalOverflow = wrapper.scrollWidth > wrapper.clientWidth + 1;
        wrapper.toggleAttribute("data-ee-overflow", hasHorizontalOverflow);
        if (hasHorizontalOverflow) {
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

    let observer = null;
    if ("ResizeObserver" in window) {
      observer = new ResizeObserver(update);
      wrappers.forEach((wrapper) => observer.observe(wrapper));
      tables.forEach((table) => observer.observe(table));
      signal.addEventListener("abort", () => observer.disconnect(), { once: true });
    }

    update();
    window.addEventListener("resize", update, { passive: true, signal });
  }

  function initialize() {
    teardown();
    const controller = new AbortController();
    teardown = () => controller.abort();
    setDocumentLanguage();
    setupSkipLink();
    setupNavigationAndSearch(controller.signal);
    setupHeaderLanguageSwitch();
    setupReadingProgress(controller.signal);
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
