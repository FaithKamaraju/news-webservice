// "use client";
import { ThemeIcon, Title } from "@mantine/core";
import { IconBrandFlipboard } from "@tabler/icons-react";
import { Group } from "@mantine/core";
import Link from "next/link";

export default function Logo() {
  return (
    <Link href="/">
      <Group align="center">
        <ThemeIcon size={"xl"}>
          <IconBrandFlipboard />
        </ThemeIcon>
        <Title order={1} size={"h3"}>
          Faith's News Feed
        </Title>
      </Group>
    </Link>
  );
}
