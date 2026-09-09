"use client";
import { useState } from "react";
import Link from "next/link";
import { ArrowRight, Search, X } from "lucide-react";
import type { CatalogItem } from "@/lib/catalog-types";

export function LibraryBrowser({ items }: { items: CatalogItem[] }) {
  const [query, setQuery] = useState("");
  const [kind, setKind] = useState("all");
  const filtered = items.filter(
    (item) =>
      (kind === "all" || item.kind === kind) &&
      `${item.title} ${item.summary} ${item.description} ${item.category}`
        .toLowerCase()
        .includes(query.toLowerCase().trim()),
  );
  return (
    <div className="library-browser">
      <div className="search-field">
        <Search size={19} aria-hidden="true" />
        <input
          aria-label="Search library"
          placeholder="Search skills, plugins, or workflows…"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        {query && (
          <button aria-label="Clear search" onClick={() => setQuery("")}>
            <X size={17} />
          </button>
        )}
      </div>
      <div className="filter-bar">
        <div className="type-filters" role="group" aria-label="Filter by type">
          {[
            ["all", "All"],
            ["skill", "Skills"],
            ["plugin", "Plugins"],
          ].map(([value, label]) => (
            <button
              key={value}
              aria-pressed={kind === value}
              onClick={() => setKind(value)}
            >
              {label}
            </button>
          ))}
        </div>
        <span aria-live="polite">{filtered.length} results</span>
      </div>
      <div className="library-heading" aria-hidden="true">
        <span>Name</span>
        <span>What it helps with</span>
        <span>Type</span>
        <span />
      </div>
      <ul className="library-list">
        {filtered.map((item) => (
          <li key={`${item.kind}-${item.slug}`}>
            <Link className="library-row" href={`/${item.kind}s/${item.slug}`}>
              <span className="row-title">
                {item.title}
                {!["active", "available"].includes(item.status) && (
                  <small>{item.status}</small>
                )}
              </span>
              <span className="row-description">
                {item.summary && item.summary !== "|"
                  ? item.summary
                  : item.description !== "|"
                    ? item.description
                    : "Read the workflow instructions and source files."}
              </span>
              <span className={`type-label ${item.kind}`}>{item.kind}</span>
              <ArrowRight size={18} aria-hidden="true" />
            </Link>
          </li>
        ))}
      </ul>
      {!filtered.length && (
        <div className="empty-state">
          <h3>No matching workflows</h3>
          <p>Try “context”, “print”, or “Shopify”, or clear your filters.</p>
          <button
            onClick={() => {
              setQuery("");
              setKind("all");
            }}
          >
            Reset filters
          </button>
        </div>
      )}
    </div>
  );
}
