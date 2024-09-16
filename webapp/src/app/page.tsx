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
          <Link href="/v1test" className="hover:underline underline-offset-4">
            Versione 1
          </Link>
        </li>
      </ul>
    </div>
  );
}
