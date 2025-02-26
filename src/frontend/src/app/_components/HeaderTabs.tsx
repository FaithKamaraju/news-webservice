"use client";
import { useState } from "react";
import { Autocomplete } from "@mantine/core";

import { IconSearch } from "@tabler/icons-react";
import { Container, Group, Tabs } from "@mantine/core";
import classes from "./HeaderTabs.module.css";

import Logo from "./Logo";

const categories = [
  "Top Stories",
  "General",
  "Science",
  "Sports",
  "Business",
  "Health",
  "Entertainment",
  "Tech",
  "Politics",
  "Food",
  "Travel",
];

export function HeaderTabs() {
  const items = categories.map((category) => (
    <Tabs.Tab value={category} key={category}>
      {category}
    </Tabs.Tab>
  ));

  return (
    <div className={classes.header}>
      <Container fluid style={{ marginBottom: "20px" }}>
        <Group align="center">
          <Logo />
          <Container fluid>
            <Autocomplete
              classNames={{ input: classes.input }}
              leftSection={<IconSearch size={16} stroke={1.5} />}
              placeholder="Search for keywords, topics, or sources"
              inputSize={"100"}
              data={["React", "Angular", "Vue", "Svelte"]}
              className={classes.search}
            />
          </Container>
          <Container fluid></Container>
        </Group>
      </Container>

      <Container size="md">
        <Tabs
          defaultValue="Home"
          variant="outline"
          // visibleFrom="sm"
          classNames={{
            root: classes.tabs,
            list: classes.tabsList,
            tab: classes.tab,
          }}
        >
          <Tabs.List>{items}</Tabs.List>
        </Tabs>
      </Container>
    </div>
  );
}
