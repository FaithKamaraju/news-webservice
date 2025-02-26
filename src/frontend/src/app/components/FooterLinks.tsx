// "use client";
import Link from "next/link";
import {
  IconBrandBluesky,
  IconBrandGithub,
  IconBrandLinkedin,
} from "@tabler/icons-react";
import { ActionIcon, Container, Group, Text } from "@mantine/core";
import Logo from "./Logo";
import classes from "./FooterLinks.module.css";

const data = [
  {
    title: "Project",
    links: [
      { label: "About", link: "/about" },
      { label: "Features", link: "/features" },
    ],
  },
];

export function FooterLinks() {
  const groups = data.map((group) => {
    const links = group.links.map((link, index) => (
      <Link key={index} href={link.link} className={classes.link}>
        {link.label}
      </Link>
    ));

    return (
      <div className={classes.wrapper} key={group.title}>
        <Text className={classes.title}>{group.title}</Text>
        {links}
      </div>
    );
  });

  return (
    <footer className={classes.footer}>
      <Container className={classes.inner}>
        <div className={classes.logo}>
          <Logo />
          <Text size="xs" c="dimmed" className={classes.description}>
            A News Feed free from distractions and with AI powered Bias
            detection.
          </Text>
        </div>
        <div className={classes.groups}>{groups}</div>
      </Container>
      <Container className={classes.afterFooter}>
        <Text c="dimmed" size="sm"></Text>

        <Group
          gap={0}
          className={classes.social}
          justify="flex-end"
          wrap="nowrap"
        >
          <ActionIcon
            component="a"
            href="https://bsky.app/profile/faithkamaraju.bsky.social"
            target="_blank"
            rel="noopener noreferrer"
            size="lg"
            color="gray"
            variant="subtle"
          >
            <IconBrandBluesky size={18} stroke={1.5} />
          </ActionIcon>
          <ActionIcon
            component="a"
            href="https://github.com/FaithKamaraju"
            target="_blank"
            rel="noopener noreferrer"
            size="lg"
            color="gray"
            variant="subtle"
          >
            <IconBrandGithub size={18} stroke={1.5} />
          </ActionIcon>
          <ActionIcon
            component="a"
            href="https://www.linkedin.com/in/faith-kamaraju-7245401b4"
            target="_blank"
            rel="noopener noreferrer"
            size="lg"
            color="gray"
            variant="subtle"
          >
            <IconBrandLinkedin size={18} stroke={1.5} />
          </ActionIcon>
        </Group>
      </Container>
    </footer>
  );
}
