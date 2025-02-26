"use client";
import { Container, Grid, SimpleGrid, Skeleton } from "@mantine/core";
import NewsCardLarge from "./NewsCardLarge";
import NewsCardSmall from "./NewsCardSmall";

const mockdata = {
  uuid: "ebd7dace-7c4c-42c5-86a8-686063801c00",
  title:
    "Experts are (literally) standing by to take your call with this service",
  description:
    "Connecting with an expert over the phone might sound old-fashioned but some say it can be the fastest way to solve your problems. JustAnswer connects people wit...",
  keywords: "",
  snippet:
    "\n\nCopied\n\nConnecting with an expert over the phone might sound old-fashioned but some say it can be the fastest way to solve your problems. JustAnswer connects ...",
  url: "https://www.today.com/video/how-justanswer-is-helping-solve-problems-with-on-call-experts-231377477999",
  image_url:
    "https://media-cldnry.s-nbcnews.com/image/upload/t_social_share_1200x630_center,f_auto,q_auto:best/mpx/2704722219/2025_02/1738939749770_tdy_money_9a_just_answer_250207_1920x1080-oj0b6u.jpg",
  language: "en",
  published_at: "2025-02-07T14:49:16.000000Z",
  source: "nbcnews.com",
  categories: ["business", "general", "tech"],
  relevance_score: null,
  locale: "us",
};

export default function NewsFeedGrid() {
  const PRIMARY_COL_HEIGHT = "400px";
  const SECONDARY_COL_HEIGHT = `calc(${PRIMARY_COL_HEIGHT} / 2 - var(--mantine-spacing-md) / 2)`;

  return (
    <Container my="md" size="xl">
      <SimpleGrid cols={{ base: 1, md: 3 }} spacing="md">
        <NewsCardLarge data={mockdata} />
        <Grid gutter="md">
          <Grid.Col>
            <NewsCardSmall data={mockdata} />
          </Grid.Col>
          <Grid.Col>
            <Skeleton
              height={SECONDARY_COL_HEIGHT}
              radius="md"
              animate={false}
            />
          </Grid.Col>
        </Grid>
        <Grid gutter="md">
          <Grid.Col>
            <Skeleton
              height={SECONDARY_COL_HEIGHT}
              radius="md"
              animate={false}
            />
          </Grid.Col>
          <Grid.Col>
            <Skeleton
              height={SECONDARY_COL_HEIGHT}
              radius="md"
              animate={false}
            />
          </Grid.Col>
        </Grid>

        <Skeleton height={PRIMARY_COL_HEIGHT} radius="md" animate={false} />
        <Grid gutter="md">
          <Grid.Col>
            <Skeleton
              height={SECONDARY_COL_HEIGHT}
              radius="md"
              animate={false}
            />
          </Grid.Col>
          <Grid.Col>
            <Skeleton
              height={SECONDARY_COL_HEIGHT}
              radius="md"
              animate={false}
            />
          </Grid.Col>
        </Grid>
        <Grid gutter="md">
          <Grid.Col>
            <Skeleton
              height={SECONDARY_COL_HEIGHT}
              radius="md"
              animate={false}
            />
          </Grid.Col>
          <Grid.Col>
            <Skeleton
              height={SECONDARY_COL_HEIGHT}
              radius="md"
              animate={false}
            />
          </Grid.Col>
        </Grid>
      </SimpleGrid>
    </Container>
  );
}
