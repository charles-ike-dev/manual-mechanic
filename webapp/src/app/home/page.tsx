"use client";

import Link from "next/link";

export default function Page() {
  return (
    <div className="p-16 flex flex-col">
      <h2 className="text-2xl mb-4">Iterazioni:</h2>
      <ul className="list-disc pl-8 gap-y-2 flex flex-col">
        <li>
          <Link href="/zerotest" className="hover:underline underline-offset-4">
            Zero Sperimentale
          </Link>
        </li>
        <li>
          <Link href="/v1" className="hover:underline underline-offset-4">
            v1: SM xml files
          </Link>
        </li>
        <li>
          <Link href="/v2" className="hover:underline underline-offset-4">
            v2: SM xml files
          </Link>
        </li>
        <li>
          <Link href="/v3" className="hover:underline underline-offset-4">
            v3: SM xml files with custom xml loader
          </Link>
        </li>
        <li>
          <Link href="/v4" className="hover:underline underline-offset-4">
            v4: SM xml files with custom xml loader (metadata strucutre updated)
          </Link>
        </li>
        <li>
          <Link href="/v5" className="hover:underline underline-offset-4">
            v5: entire eTim folder
          </Link>
        </li>
        <li>
          <Link href="/v6" className="hover:underline underline-offset-4">
            v6: only pdf and xml
          </Link>
        </li>
        <li>
          <Link href="/v7" className="hover:underline underline-offset-4">
            v7: entire eTim folder + Custom XML loader
          </Link>
        </li>
        <li>
          <Link href="/v8" className="hover:underline underline-offset-4">
            v8: uploaded the entire eTim folder + missing SM xml files
          </Link>
        </li>
        <li>
          <Link href="/v9" className="hover:underline underline-offset-4">
            v9: uploaded the correct files (missing pip and sm)
          </Link>
        </li>
        <li>
          <Link href="/v11" className="hover:underline underline-offset-4">
            v11 fix: bugfix filename and sources
          </Link>
        </li>{" "}
        <li>
          <Link href="/v12" className="hover:underline underline-offset-4">
            v12 nopip: temporary removed PIP files to check improvements
          </Link>
        </li>{" "}
        <li>
          <Link href="/v13" className="hover:underline underline-offset-4">
            v13: frontend improvements, bugfixes and PIP files re-added, adding
            S-WAY AS in the systemprompt
          </Link>
        </li>
        <li>
          <Link href="/v14" className="hover:underline underline-offset-4">
            v14: adding docs in txt format
          </Link>
        </li>
      </ul>
    </div>
  );
}
